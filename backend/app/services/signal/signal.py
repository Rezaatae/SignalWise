import math
import pandas as pd
import numpy as np
import collections
from itertools import islice
from collections import deque
from app.schemas.signal import SignalResponse

class Signal:
    def __init__(self, strategyType, strategyConfig):
        self.strategyType=strategyType
        self.strategyConfig=strategyConfig
        self._fast_ma_window=strategyConfig.fast_ma_window
        self._slow_ma_window=strategyConfig.slow_ma_window
        self._fast_price_deque=deque([], maxlen=self._fast_ma_window)
        self._slow_price_deque=deque([], maxlen=self._slow_ma_window)

    def generate_signal(self, price):
        return self.generate_MACrossover_signal(price)
    
    def generate_MACrossover_signal(self, price):
        self._fast_price_deque.append(price.close)
        self._slow_price_deque.append(price.close)
        signal=None
        if len(self._slow_price_deque) < self._slow_ma_window:
            signal = SignalResponse(direction=8888, timestamp=price.timestamp)
        else:
            fast_ma=sum(self._fast_price_deque)/len(self._fast_price_deque) # fast ma
            slow_ma=sum(self._slow_price_deque)/len(self._slow_price_deque) # slow ma
            if fast_ma > slow_ma:
                signal = SignalResponse(direction=-1, timestamp=price.timestamp)
            elif fast_ma < slow_ma:
                signal = SignalResponse(direction=1, timestamp=price.timestamp)
            else:
                signal = SignalResponse(direction=0, timestamp=price.timestamp)
        return signal