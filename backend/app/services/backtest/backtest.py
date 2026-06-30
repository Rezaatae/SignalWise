from app.services.data.data import Data
from app.services.signal.signal import Signal
from app.services.portfolio.portfolio import Portfolio
from app.services.execution.execution import Execution
from app.services.analytics.analytics import Analytics
from app.schemas.strategy import MACrossoverRequest
from app.services.data.quotes import simulate_quote
from app.services.execution.fills import FillSimulator 
from app.services.execution.costs import PercentageCostModel
from app.services.execution.latency import FixedLatencyModel 


class Backtest:
    def __init__(self, instrument: str, strategyType: str, strategyConfig: MACrossoverRequest):
        self.instrument = instrument
        self.strategyType = strategyType
        self.strategyConfig = strategyConfig
        self.latency_model =  FixedLatencyModel()
        self.cost_model = PercentageCostModel()
        self.fill_simulator = FillSimulator()

    def run(self):
        test_return_value = []
        data_source = Data(instrument=self.instrument, startDate=self.strategyConfig.start_date, endDate=self.strategyConfig.end_date)
        signal_engine = Signal(strategyType=self.strategyType, strategyConfig=self.strategyConfig)
        portfolio = Portfolio()
        execution_engine = Execution(self.latency_model, self.cost_model, self.fill_simulator)
        # analytics_engine = Analytics()
        
        market_data = data_source.get_market_data()

        for row in market_data.data:
            market_quote = simulate_quote(self.instrument, row.timestamp, row.open, row.volume)
            signal = signal_engine.generate_signal(price=row)
            if signal.isNewSignal:
                target_position = portfolio.construct_target_position(signal)
                order = portfolio.create_order(target_position)
                execution_engine.submit_order(order)
            fills = execution_engine.process_orders(market_quote)
            portfolio.update(fills)
            test_return_value.append(portfolio.get_portfolio_state())
            # analytics_engine.record(portfolio)
        return test_return_value