from app.services.execution.execution import Execution
from app.services.execution.fills import FillSimulator
from app.services.execution.costs import PercentageCostModel
from app.services.execution.latency import FixedLatencyModel
from app.schemas.order import Order, OrderType, OrderStatus
from datetime import datetime

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
    