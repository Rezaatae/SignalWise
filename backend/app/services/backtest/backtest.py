from app.services.data.data import Data
from app.services.signal.signal import Signal
from app.services.portfolio.portfolio import Portfolio
from app.services.execution.execution import Execution
from app.services.analytics.analytics import Analytics

class Backtest:
    def __int__(self, instrument, strategyType, strategyConfig):
        self.instrument = instrument
        self.strategy = strategyType
        self.strategyConfig = strategyConfig

    def run(self):
        data_source = Data(instrument=self.instrument, startDate=self.strategyConfig.start_date, endDate=self.strategyConfig.end_date)
        signal_engine = Signal(strategyType=self.strategyType)
        portfolio = Portfolio()
        execution_engine = Execution()
        analytics_engine = Analytics()
        
        market_data = data_source.get_market_data()

        for row in market_data:
            signal = signal_engine.generate_signal(priceData=row)
            target_position = portfolio.construct_position(signal)
            order = portfolio.create_order(target_position)
            fill = execution_engine.execute(order)
            portfolio.update(fill)
            analytics_engine.record(portfolio)