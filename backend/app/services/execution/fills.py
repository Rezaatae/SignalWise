from app.schemas.order import Order, Quote, OrderType

class FillSimulator:

    def fill_order(self, order: Order, quote: Quote) -> tuple[int, float]:
        if order.order_type == OrderType.BUY:
            executable_qty = min(order.remaining_quantity, quote.available_ask_size)
            price = quote.ask
        else:
            executable_qty = min(order.remaining_quantity, quote.available_bid_size)
            price = quote.bid

        return executable_qty, price