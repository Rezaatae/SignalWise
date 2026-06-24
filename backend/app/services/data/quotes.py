from datetime import datetime
from app.schemas.order import Quote


def simulate_quote(instrument: str, timestamp: datetime, reference_price: float, daily_volume: int, spread_bps: float = 5.0, liquidity_pct: float = 0.05) -> Quote:
    """
    Create a synthetic quote from OHLCV data.

    spread_bps:
        Total spread in basis points.
        Example: 5 bps = 0.05%

    liquidity_pct:
        Fraction of daily volume considered immediately available.
        Example: 0.05 = 5%
    """

    spread_fraction = spread_bps / 10000

    half_spread = reference_price * spread_fraction / 2

    bid = round(reference_price - half_spread, 4)
    ask = round(reference_price + half_spread, 4)

    available_size = int(daily_volume * liquidity_pct)

    return Quote(
        instrument=instrument,
        timestamp=timestamp,
        bid=bid,
        ask=ask,
        available_bid_size=available_size,
        available_ask_size=available_size,
    )