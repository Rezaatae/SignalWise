from app.schemas.signal import SignalResponse
from app.schemas.order import Position, Order, OrderType, Fill
from datetime import datetime
from app.schemas.ohlvc import OHLCV
from app.schemas.analytics import EquityCurve
from typing import List

#todo: generate - TradeHistory
# PortfolioHistory
# EquityCurve
# ReturnsSeries

class Portfolio:
    def __init__(self, cash: float=250000.00, positions: dict[str, Position]={}):
        self.cash=cash
        self.positions=positions
        # self.holdings=holdings #todo
        self.equity=self.cash + sum([position.unrealizedPnL for position in self.positions.values()])
        self.pnl=0
        self.last_update = datetime.now()
        self.equity_series: List[EquityCurve] = []

    def get_portfolio_state(self) -> dict[float, dict, float, float]:
        return {"timestamp": self.last_update, "cash":self.cash, "positions":self.positions, "equity":self.equity, "pnl":self.pnl}

    def construct_target_position(self, signal: SignalResponse) -> Position:
        signal_direction = signal.direction
        is_asset_held = signal.instrument in self.positions
        target_allocation = 0
        if signal.isNewSignal:
            if signal_direction == 1:
                target_allocation=self.cash//signal.sharePrice.close
            elif signal_direction == -1:
                target_allocation=0 if not is_asset_held else -self.positions[signal.instrument].quantity
            else:
                target_allocation = 0
        return Position(instrument=signal.instrument, quantity=target_allocation, marketPrice=signal.sharePrice.close, costHistory=[])

    def create_order(self, targetPosition: Position) -> Order:
        order_type = None
        order_quantity = 0
        if targetPosition.quantity > 0:
            # calculate shares to buy
            order_type = OrderType.BUY
            order_quantity=abs(targetPosition.quantity)
        elif targetPosition.quantity < 0:
            # calculate shares to sell
            order_type = OrderType.SELL
            order_quantity=abs(targetPosition.quantity)
        else:
            order_type = OrderType.HOLD
            order_quantity=abs(targetPosition.quantity)
        return Order(instrument=targetPosition.instrument, 
                     order_type=order_type, 
                     quantity=order_quantity, 
                     created_at=datetime.now())
    
    def update(self, fills: list[Fill], price: OHLCV, instrument: str):
        if fills:
            self._update_portfolio_with_fills(fills)
        else:
            self._update_portfolio_with_market_price(price, instrument)
        self.last_update = datetime.now()
        curr_state=self.get_portfolio_state()
        if not self.equity_series:
            self.equity_series=[EquityCurve(timestamp=curr_state["timestamp"], equity=curr_state["equity"])]
        else:
            self.equity_series.append(EquityCurve(timestamp=curr_state["timestamp"], equity=curr_state["equity"]))

    def _update_portfolio_with_market_price(self, price: OHLCV, instrument: str):
        if instrument in self.positions:
            self.positions[instrument].costHistory.append(price.close)
            self.positions[instrument].marketPrice = price.close
        self.equity=self.cash + sum([position.unrealizedPnL for position in self.positions.values()])


    def _update_portfolio_with_fills(self, fills: list[Fill]):
        for fill in fills:
            trade_value = (fill.price * fill.quantity) - fill.commission
            trade_cost = (fill.price * fill.quantity) + fill.commission
            if fill.order_type == OrderType.BUY:
                # update cash
                self.cash -= trade_cost
                # update positions
                if fill.instrument not in self.positions:
                    self.positions[fill.instrument] = Position(instrument=fill.instrument, quantity=fill.quantity, marketPrice=fill.price, costHistory=[fill.price])
                else:
                    self.positions[fill.instrument].quantity += fill.quantity
                    self.positions[fill.instrument].costHistory.append(fill.price)
                    self.positions[fill.instrument].marketPrice = fill.price
                # update equity
                self.equity=self.cash + sum([position.unrealizedPnL for position in self.positions.values()])
            else: # fill.order_type == OrderType.SELL
                # update cash
                self.cash += trade_value
                #update price
                self.positions[fill.instrument].marketPrice = fill.price
                self.positions[fill.instrument].costHistory.append(fill.price)
                # update pnl
                self.pnl+=self.positions[fill.instrument].unrealizedPnL
                # update positon quantity
                self.positions[fill.instrument].quantity -= fill.quantity
                # update equity
                self.equity=self.cash + sum([position.unrealizedPnL for position in self.positions.values()])
