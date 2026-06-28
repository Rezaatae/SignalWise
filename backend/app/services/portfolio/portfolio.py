from app.schemas.signal import SignalResponse
from app.schemas.order import Position, Order, OrderType
from datetime import datetime

class Portfolio:
    def __init__(self):
        self.cash=250000.00
        self.holdings: dict[str, int]={} # {instrument: str, shares: int}
        self.equity=250000.00
        pass

    def get_portfolio_state(self) -> dict[int, dict, int]:
        return {"cash":self.cash, "holdings":self.holdings, "equity":self.equity}

    def construct_target_position(self, signal: SignalResponse) -> Position:
        signal_direction = signal.direction
        target_allocation = 0
        if signal.isNewSignal:
            if signal_direction == 1:
                target_allocation = 100
            elif signal_direction == -1:
                target_allocation = -100
            else:
                target_allocation = 0
        return Position(instrument=signal.instrument, allocation=target_allocation, price=signal.sharePrice)

    def create_order(self, targetPosition: Position) -> Order:
        is_asset_held = targetPosition.instrument in self.holdings
        order_type = None
        order_shares = 0
        order_allocation = targetPosition.allocation/100
        if targetPosition.allocation > 0:
            # calculate shares to buy
            order_shares=(self.cash * order_allocation)//targetPosition.price.close if not is_asset_held else self.holdings[targetPosition.instrument] - self.cash//targetPosition.price.close
            order_type = OrderType.BUY
        elif targetPosition.allocation < 0:
            # calculate shares to buy
            order_type = OrderType.SELL
            order_shares=self.holdings[targetPosition.instrument] * order_allocation if is_asset_held else 0
        else:
            order_type = OrderType.HOLD
            order_shares=self.holdings[targetPosition.instrument] if is_asset_held else 0
        return Order(instrument=targetPosition.instrument, 
                     order_type=order_type, 
                     quantity=order_shares, 
                     created_at=datetime.now())

    def update(self):
        pass