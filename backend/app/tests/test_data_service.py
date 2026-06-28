from app.services.data.data import Data

def test_get_market_data_returns_OHLCV():
    data_layer = Data(instrument='AAPL', startDate='2010-06-24', endDate='2011-06-24')
    result = data_layer.get_market_data()

    # Core fields (OHLCV, timestamp) always present
    assert len(result.data) > 0
    assert hasattr(result.data[0], "timestamp")
    assert hasattr(result.data[0], "open")
    assert hasattr(result.data[0], "high")
    assert hasattr(result.data[0], "low")
    assert hasattr(result.data[0], "close")
    assert hasattr(result.data[0], "volume")