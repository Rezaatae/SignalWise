class PercentageCostModel:
    """
    Transaction costs expressed percentage of trade value.

    Example:
        commission_rate = 0.25%

        £10,000 trade
        cost = £25.00
    """

    def __init__(self, commission_rate: float=0.25):
        self.commission_rate = commission_rate

    def calculate(self, trade_value: float) -> float:
        return trade_value * self.commission_rate / 100