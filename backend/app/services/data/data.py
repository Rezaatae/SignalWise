from app.clients.yahoo_finance import get_daily_prices

from app.services.adapters.yf_adapter import yf_raw_to_ohlcv

class Data:
    def __init__(self, instrument: str, startDate, endDate):
        self.instrument = instrument
        self.startDate = startDate
        self.endDate = endDate

    def get_market_data(self):
        raw = get_daily_prices(self.instrument, self.startDate, self.endDate)
        return yf_raw_to_ohlcv(self.instrument, raw)