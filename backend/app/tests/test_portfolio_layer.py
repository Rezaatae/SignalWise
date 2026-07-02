from app.services.portfolio.portfolio import Portfolio
from app.schemas.signal import SignalResponse
from app.schemas.ohlvc import OHLCV
from datetime import datetime
from app.schemas.order import Position, Order, OrderType, Fill


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

def test_portfolio_updates_with_fill():
    test_fill_list = [
    {
      "order_id": "18bce87b-8d26-46c6-9115-9bf824e467bc",
      "instrument": "AAPL",
      "quantity": 25136,
      "price": 9.9345,
      "commission": 624.28398,
      "timestamp": "2011-06-08T00:00:00"
    }
  ]
    portfolio = Portfolio()
    pass