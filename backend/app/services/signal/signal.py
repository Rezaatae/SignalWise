import math
import pandas as pd
import numpy as np

class Signal:
    def __init__(self, priceData, strategyType, strategyConfig):
        self.strategyType=strategyType
        self.strategyConfig=strategyConfig
        self.priceData=priceData
        self.priceDataList=[]

    def generate_signal(self, price_data):
        self.priceDataList.append(price_data)
        if self.strategyType=="MACrossover":
            return self.generate_MACrossover_signal(self.priceDataList, self.strategyConfig)
    
    def generate_MACrossover_signal(self, price_list, config):
        if len(price_list) < config["slow_ma"]:
            return "HOLD"
        if len(price_list) >= config["slow_ma"]:
            sma1=price_list.rolling(window=config["fast_ma"]).mean()
            sma2=price_list.rolling(window=config["slow_ma"]).mean()
            if sma1[-1] > sma2[-1]: # most likely wrong, just scaffolding
                return "BUY"
            elif sma1[-1] < sma2[-1]:
                return "SELL"
            else:
                return "HOLD"
    
    def clear_price_data(self):
        self.priceDataList.clear()