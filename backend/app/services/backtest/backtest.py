from app.services.data.data import Data
from app.services.signal.signal import Signal
from app.services.portfolio.portfolio import Portfolio
from app.services.execution.execution import Execution
from app.services.analytics.analytics import Analytics

class Backtest:
    def __int__(self, strategy, strategyConfig):
        self.strategy = strategy
        self.strategyConfig = strategyConfig

    def run(self):
        data_source = Data()
        signal_engine = Signal()
        portfolio = Portfolio()
        execution_engine = Execution()
        analytics_engine = Analytics()
        
        market_data = data_source.get_market_data() # get market_data from client

        for row in market_data:
            signal = signal_engine.generate_signal(market_state=row)
            target_position = portfolio.construct_position(signal)
            order = portfolio.create_order(target_position)
            fill = execution_engine.execute(order)
            portfolio.update(fill)
            analytics_engine.record(portfolio)