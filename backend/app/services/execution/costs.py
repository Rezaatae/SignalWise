class PercentageCostModel:
    """
    Transaction costs expressed in basis points (bps).

    Example:
        commission_bps = 1.0

        £10,000 trade
        cost = £1.00
    """

    def __init__(self, commission_bps: float):
        self.commission_bps = commission_bps

    def calculate(self, notional: float) -> float:
        return notional * self.commission_bps / 10_000