from app.services.portfolio.portfolio import Portfolio
from app.schemas.signal import SignalResponse
from app.schemas.ohlvc import OHLCV
from app.schemas.order import Position, OrderType, Fill


def test_portfolio_creates_buy_target_position_from_signal():
    portfolio = Portfolio()
    test_price_data = OHLCV(timestamp='2011-06-15 00:00:00', 
                            open=9.871205651492119,
                            high=9.887670110974701,
                            low=9.725419605392474,
                            close=9.781399726867676,
                            volume=399196000.0)
    test_buy_signal = SignalResponse(instrument='AAPL', sharePrice=test_price_data, direction=1, isNewSignal=True)

    target_position = portfolio.construct_target_position(test_buy_signal)

    assert target_position.instrument == 'AAPL'
    assert target_position.quantity == portfolio.cash//9.781399726867676
    assert target_position.costHistory == []
    assert target_position.marketPrice == 9.781399726867676

def test_portfolio_creates_sell_target_position_from_signal():
    test_price_data = OHLCV(timestamp='2011-06-15 00:00:00', 
                            open=9.871205651492119,
                            high=9.887670110974701,
                            low=9.725419605392474,
                            close=9.781399726867676,
                            volume=399196000.0)
    existing_position = Position(instrument='AAPL', quantity=100, marketPrice=test_price_data.close, costHistory=[])
    portfolio = Portfolio(cash=250000.00, positions={'AAPL':existing_position})
    test_sell_signal = SignalResponse(instrument='AAPL', sharePrice=test_price_data, direction=-1, isNewSignal=True)

    target_position = portfolio.construct_target_position(test_sell_signal)

    assert target_position.instrument == 'AAPL'
    assert target_position.quantity == -100
    assert target_position.costHistory == []
    assert target_position.marketPrice == 9.781399726867676

def test_portfolio_creates_buy_order_from_target_positiom():
    portfolio = Portfolio()
    test_price_data = OHLCV(timestamp='2011-06-15 00:00:00', 
                            open=9.871205651492119,
                            high=9.887670110974701,
                            low=9.725419605392474,
                            close=9.781399726867676,
                            volume=399196000.0)
    
    test_sell_signal = SignalResponse(instrument='AAPL', sharePrice=test_price_data, direction=1, isNewSignal=True)
    target_position = portfolio.construct_target_position(test_sell_signal)
    order = portfolio.create_order(targetPosition=target_position)

    assert order.instrument == 'AAPL'
    assert order.order_type == OrderType.BUY
    assert order.quantity == 250000.00//9.781399726867676

def test_portfolio_creates_sell_order_from_target_positiom():
    test_price_data = OHLCV(timestamp='2011-06-15 00:00:00', 
                            open=9.871205651492119,
                            high=9.887670110974701,
                            low=9.725419605392474,
                            close=9.781399726867676,
                            volume=399196000.0)
    existing_position = Position(instrument='AAPL', quantity=100, marketPrice=test_price_data.close, costHistory=[])
    portfolio = Portfolio(cash=250000.00, positions={'AAPL':existing_position})
    test_sell_signal = SignalResponse(instrument='AAPL', sharePrice=test_price_data, direction=-1, isNewSignal=True)
    target_position = portfolio.construct_target_position(test_sell_signal)

    order = portfolio.create_order(targetPosition=target_position)

    assert order.instrument == 'AAPL'
    assert order.order_type == OrderType.SELL
    assert order.quantity == 100

def test_portfolio_updates_with_buy_fills():
    existing_position = Position(instrument='AAPL', quantity=100, marketPrice=30.0, costHistory=[30.0])
    portfolio = Portfolio(cash=250000.00, positions={'AAPL':existing_position})
    test_fills_list = [Fill(order_id='89644b0a-d415-4a92-a6f2-10f53dec1ef5',
            order_type=OrderType.BUY,
            instrument="AAPL",
            quantity= 100,
            price= 20.0,
            commission = 5.0,
            timestamp= "2011-06-08T00:00:00"),
            Fill(order_id='b64a7d01-4a7d-482e-86e8-0bcafec1ad0b',
            order_type=OrderType.BUY,
            instrument="MCSFT",
            quantity= 300,
            price= 25.0,
            commission = 18.75,
            timestamp= "2011-06-08T00:00:00")]

    portfolio.update(test_fills_list)
    portfolio_state = portfolio.get_portfolio_state()
    assert portfolio_state['cash'] == 240476.25 # cash - trade cost
    assert 'AAPL' in portfolio_state["positions"]
    assert 'MCSFT' in portfolio_state["positions"]
    assert portfolio_state["positions"]['AAPL'].quantity == 200
    assert portfolio_state["positions"]['MCSFT'].quantity == 300
    assert portfolio_state["equity"] ==  240476.25 + portfolio_state["positions"]['AAPL'].unrealizedPnL + portfolio_state["positions"]['MCSFT'].unrealizedPnL # cash + unrealizedPnL
    assert portfolio_state["pnl"] == 0

def test_portfolio_updates_with_sell_fills():
    existing_AAPL_position = Position(instrument='AAPL', quantity=100, marketPrice=10.0, costHistory=[10.0])
    existing_MCSFT_position = Position(instrument='MCSFT', quantity=100, marketPrice=30.0, costHistory=[30.0])
    portfolio = Portfolio(cash=250000.00, positions={'AAPL':existing_AAPL_position,
                                                     'MCSFT': existing_MCSFT_position})
    test_fills_list = [Fill(order_id='89644b0a-d415-4a92-a6f2-10f53dec1ef5',
            order_type=OrderType.SELL,
            instrument="AAPL",
            quantity= 100,
            price= 20.0,
            commission = 5.0,
            timestamp= "2011-06-08T00:00:00"),
            Fill(order_id='b64a7d01-4a7d-482e-86e8-0bcafec1ad0b',
            order_type=OrderType.SELL,
            instrument="MCSFT",
            quantity= 100,
            price= 10.0,
            commission = 2.5,
            timestamp= "2011-06-08T00:00:00")]
    
    portfolio.update(test_fills_list)
    portfolio_state = portfolio.get_portfolio_state()

    assert portfolio_state['cash'] == 252992.5 # current cash + trade values (commission goes to broker)
    assert portfolio_state["positions"]['AAPL'].quantity == 0
    assert portfolio_state["positions"]['MCSFT'].quantity == 0
    assert portfolio_state["equity"] == 252992.5 # only cash when no stocks remaining
    assert portfolio_state["pnl"] == -500 # sum of realised pnl (realised pnl = unrealised pnl at time of trade)