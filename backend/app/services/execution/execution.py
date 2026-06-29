from app.schemas.order import Order, Fill, OrderStatus, Quote
from typing import List

class Execution:
    def __init__(self, latency_model, cost_model, fill_simulator):
        self.latency_model = latency_model
        self.cost_model = cost_model
        self.fill_simulator = fill_simulator
        self.orders: dict[str, Order] = {}
        pass

    def submit_order(self, order: Order):
        order.status=OrderStatus.PENDING
        self.orders[order.order_id] = order

    def process_orders(self, quote: Quote) -> List[Fill]:
        fills = []
        for order in self.orders.values():
            if order.instrument != quote.instrument:
                continue
            if order.status == OrderStatus.FILLED:
                continue
            qty, price, order_type = self.fill_simulator.fill_order(order, quote)

            if qty == 0:
                continue

            commission = self.cost_model.calculate(qty*price)

            fill = Fill(
                order_id=order.order_id,
                order_type=order_type,
                instrument=order.instrument,
                quantity=qty,
                price=price,
                commission=commission,
                timestamp=quote.timestamp
            )

            order.filled_quantity += qty

            if order.filled_quantity >= order.quantity:
                order.status = OrderStatus.FILLED
            else:
                order.status = OrderStatus.PARTIALLY_FILLED
            fills.append(fill)
        return fills
        
