import pandas as pd
from app.schemas.ohlvc import OHLCV, OHLCVSeries

def yf_raw_to_ohlcv(instrument, raw_data):
    skipped = 0
    result = []
    if 'Close' and 'High' and 'Low' and 'Close' and 'Volume' not in raw_data:
        raise Exception("Data Missing Target Column(s)")
    
    try:
        flat_data = keep_column_level(raw_data)
    except Exception as e:
             print(f"Error flattening dataframe: {e}")


    for date, price in flat_data.iterrows():
        try:
            if any(price[field] in ["N/A", "", None] or pd.isna(price[field])
                    for field in ['Close', 'High', 'Low', 'Open', 'Volume']):
                skipped += 1
                continue
            price_point = OHLCV(
                    timestamp=date,
                    open=float(price["Open"]),
                    high=float(price["High"]),
                    low=float(price["Low"]),
                    close=float(price["Close"]),
                    volume=float(price["Volume"]),
                )
            result.append(price_point)
        except Exception as e:
             skipped += 1
             print(f"Skipped row {date}: {price} | Error: {e}")
    return OHLCVSeries(
        symbol=instrument,
        data=result
    )
    
def is_invalid(value: str):
    return value in ("N/A", "", None)

def keep_column_level(df, target_cols=['Close', 'High', 'Low', 'Open', 'Volume']):
    target_cols = set(map(str, target_cols))

    if not isinstance(df.columns, pd.MultiIndex):
        return df

    for level in range(df.columns.nlevels):
        vals = set(map(str, df.columns.get_level_values(level)))

        if target_cols.issubset(vals):
            df = df.copy()
            df.columns = df.columns.get_level_values(level)
            return df

    raise ValueError(
        f"No level contains all columns: {target_cols}"
    )
