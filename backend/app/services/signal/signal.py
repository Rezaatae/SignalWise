from collections import deque
from app.schemas.signal import SignalResponse
from app.schemas.ohlvc import OHLCV

class Signal:
    def __init__(self, strategyType, strategyConfig):
        self.strategyType=strategyType
        self.strategyConfig=strategyConfig
        self.instrument=strategyConfig.instrument
        self._fast_ma_window=strategyConfig.fast_ma_window
        self._slow_ma_window=strategyConfig.slow_ma_window
        self._fast_price_deque=deque([], maxlen=self._fast_ma_window)
        self._slow_price_deque=deque([], maxlen=self._slow_ma_window)
        self.last_signal_direction=None

    def generate_signal(self, price: OHLCV):
        return self.generate_MACrossover_signal(price)
    
    def generate_MACrossover_signal(self, price: OHLCV):
        is_new_signal=False
        signal_direction=3
        self._fast_price_deque.append(price.close)
        self._slow_price_deque.append(price.close)
        if len(self._slow_price_deque) < self._slow_ma_window:
            pass
        else:
            fast_ma=sum(self._fast_price_deque)/len(self._fast_price_deque)
            slow_ma=sum(self._slow_price_deque)/len(self._slow_price_deque)
            if fast_ma > slow_ma:
                signal_direction=1
            elif fast_ma < slow_ma:
                signal_direction=-1
            else:
                signal_direction=0
            
            if (signal_direction!=self.last_signal_direction):
                is_new_signal=True
                self.last_signal_direction=signal_direction
                
        return SignalResponse(instrument=self.instrument, sharePrice=price, direction=signal_direction, isNewSignal=is_new_signal)