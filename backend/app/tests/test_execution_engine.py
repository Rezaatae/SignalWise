from app.services.execution.execution import Execution
from app.services.portfolio.portfolio import Portfolio
from app.services.execution.fills import FillSimulator
from app.services.execution.costs import PercentageCostModel
from app.services.execution.latency import FixedLatencyModel
from app.schemas.order import Order, OrderType, OrderStatus
from datetime import datetime
from app.schemas.ohlvc import OHLCV
from app.services.data.quotes import simulate_quote


def test_submitted_orders_are_pending():
    test_order = Order(instrument='AAPL', 
                     order_type=OrderType.BUY, 
                     quantity=100, 
                     created_at=datetime.now())
    latency_model =  FixedLatencyModel()
    cost_model = PercentageCostModel()
    fill_simulator = FillSimulator()
    execution_engine = Execution(latency_model, cost_model, fill_simulator)

    execution_engine.submit_order(test_order)
    submitted_orders = execution_engine.orders

    assert len(submitted_orders) == 1
    assert submitted_orders[test_order.order_id].status == OrderStatus.PENDING

def test_generated_quotes():
    test_price_data = OHLCV(timestamp='2011-06-15 00:00:00', 
                            open=20.0,
                            high=30.0,
                            low=10.00,
                            close=25.0,
                            volume=500000000.0)
    test_market_quote = simulate_quote(
        'AAPL', 
        test_price_data.timestamp, 
        test_price_data.open, 
        test_price_data.volume
        ) # spread_bps = 5.0, liquidity_pct = 0.05
    
    assert test_market_quote.instrument == 'AAPL'
    assert test_market_quote.bid == 19.995 # reference_price - half_spread
    assert test_market_quote.ask == 20.005 # reference_price + half_spread
    assert test_market_quote.available_bid_size == 25000000 # daily_volume * liquidity_pct
    assert test_market_quote.available_ask_size == 25000000 # daily_volume * liquidity_pct

def test_fill_simulator_fills_buy_orders():
    fill_simulator = FillSimulator()
    test_price_data = OHLCV(timestamp='2011-06-15 00:00:00', 
                            open=20.0,
                            high=30.0,
                            low=10.00,
                            close=25.0,
                            volume=500000000.0)
    test_sell_order = Order(instrument='AAPL', 
                     order_type=OrderType.BUY, 
                     quantity=100, 
                     created_at='2011-06-15 00:00:00')
    test_market_quote = simulate_quote('AAPL', 
                                       test_price_data.timestamp, 
                                       test_price_data.open, 
                                       test_price_data.volume)

    qty, price, order_type = fill_simulator.fill_order(test_sell_order, test_market_quote)

    assert qty == 100
    assert price == 20.005
    assert order_type == 'BUY'

def test_fill_simulator_fills_sell_orders():
    fill_simulator = FillSimulator()
    test_price_data = OHLCV(timestamp='2011-06-15 00:00:00', 
                            open=20.0,
                            high=30.0,
                            low=10.00,
                            close=25.0,
                            volume=500000000.0)
    test_sell_order = Order(instrument='AAPL', 
                     order_type=OrderType.SELL, 
                     quantity=100, 
                     created_at='2011-06-15 00:00:00')
    test_market_quote = simulate_quote('AAPL', 
                                       test_price_data.timestamp, 
                                       test_price_data.open, 
                                       test_price_data.volume)

    qty, price, order_type = fill_simulator.fill_order(test_sell_order, test_market_quote)

    assert qty == 100
    assert price == 19.995
    assert order_type == 'SELL'

def test_cost_model_calculates_commission():
    cost_model = PercentageCostModel()

    test_qty = 100
    test_price = 20.0

    commission = cost_model.calculate(test_qty*test_price)

    assert commission == 5.0 # trade_value * commision_rate


def test_process_orders_generates_buy_fills():
    latency_model =  FixedLatencyModel()
    cost_model = PercentageCostModel()
    fill_simulator = FillSimulator()
    execution_engine = Execution(latency_model, cost_model, fill_simulator)
    test_price_data = OHLCV(timestamp='2011-06-15 00:00:00', 
                            open=20.0,
                            high=30.0,
                            low=10.00,
                            close=25.0,
                            volume=500000000.0)
    test_buy_order = Order(instrument='AAPL', 
                     order_type=OrderType.BUY, 
                     quantity=100, 
                     created_at='2011-06-15 00:00:00')
    test_market_quote = simulate_quote('AAPL', 
                                       test_price_data.timestamp, 
                                       test_price_data.open, 
                                       test_price_data.volume)
    execution_engine.submit_order(test_buy_order)

    fills=execution_engine.process_orders(test_market_quote)

    assert len(fills)==1
    assert fills[0].instrument == 'AAPL'
    assert fills[0].order_type == 'BUY'
    assert fills[0].price == 20.005
    assert fills[0].quantity == 100

    