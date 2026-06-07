import math
import pandas as pd
import numpy as np
import collections
from collections import deque
from app.schemas.signal import SignalResponse

class Signal:
    def __init__(self, strategyType, strategyConfig):
        self.strategyType=strategyType
        self.strategyConfig=strategyConfig
        self._fast_ma_window=strategyConfig.fast_ma_window
        self._slow_ma_window=strategyConfig.slow_ma_window
        self._price_deque=deque([], maxlen=self._fast_ma_window)

    def generate_signal(self, price):
        return self.generate_MACrossover_signal(price, self.strategyConfig)
    
    def generate_MACrossover_signal(self, price, config):
        self._price_deque.append(price.close)
        signal=None
        if len(self._price_deque) < config.fast_ma_window:
            signal = SignalResponse(direction=8888, timestamp=price.timestamp)
        else:
            slow_ma_price_list = list(self._price_deque)[-self._slow_ma_window:]
            fast_ma=sum(self._price_deque)/len(self._price_deque) # fast ma
            slow_ma=sum(slow_ma_price_list)/len(slow_ma_price_list) # slow ma
            if fast_ma > slow_ma:
                signal = SignalResponse(direction=-1, timestamp=price.timestamp)
            elif fast_ma < slow_ma:
                signal = SignalResponse(direction=1, timestamp=price.timestamp)
            else:
                signal = SignalResponse(direction=0, timestamp=price.timestamp)
        return signal