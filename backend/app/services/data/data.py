import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf

class Data:
    def __init__(self, instrument: str, startDate, endDate):
        self.instrument = instrument
        self.startDate = startDate
        self.endDate = endDate

    def get_market_data(self):
        # pass through adapter first
        return yf.download(
            self.instrument,
            start=self.startDate,
            end=self.startDate,
            auto_adjust=True
            ).Close[self.instrument]