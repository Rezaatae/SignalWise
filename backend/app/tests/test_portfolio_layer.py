from app.services.portfolio.portfolio import Portfolio


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