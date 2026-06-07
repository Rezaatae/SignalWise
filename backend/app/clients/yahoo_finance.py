import yfinance as yf

def get_daily_prices(instrument, startDate, endDate):
    return yf.download(
            instrument,
            start=startDate,
            end=endDate,
            auto_adjust=True,
            interval="1d"
            )