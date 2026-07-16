import numpy as np
import pandas as pd
from app.services.portfolio.portfolio import Portfolio
from app.schemas.analytics import EquityCurve, BacktestResult

# todo: generate - Sharpe
# Sortino
# Max Drawdown
# Volatility
# CAGR
# Win Rate - from portfolio data


class Analytics:
    def __init__(self):
        pass

    def record(self, portfolio: Portfolio):
        equity_curve_data = portfolio.equity_series
        return self.calc(equity_curve_data)

    def calc(self, data):
        df = pd.DataFrame.from_records([obj.__dict__ for obj in data])
        df["Date"] = pd.to_datetime(df["timestamp"])
        df.set_index("Date", inplace=True)

        df.sort_index(inplace=True)

        df["Returns"] = np.log(df["equity"] / df["equity"].shift(1))
        clean_returns = df["Returns"].dropna().tolist()
        daily_vol = df["Returns"].dropna().std()
        annualized_vol = daily_vol * np.sqrt(252)
        return BacktestResult(ec=data,
                              daily_vol=daily_vol,
                              daily_returns=clean_returns,
                              vol=annualized_vol)
