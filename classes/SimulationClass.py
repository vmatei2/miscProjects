import datetime
import random
import yfinance as yf
from classes.InvestorTypes import InvestorTypes
from classes.MarketEnvironment import MarketEnvironment
from classes.Trader import Trader
from classes.helpers import select_closing_prices, get_price_history


class SimulationClass:
    def __init__(self, time_steps, N_agents, market_environment):
        self.N_agents = int(N_agents)
        self.time_steps = time_steps
        self.market_environment = market_environment
        self.agents = self.create_agents()

    def create_agents(self):
        agents = {}
        investor_type = [InvestorTypes.SHORT_TERM, InvestorTypes.LONGTERM]
        investor_type_probabilities = [0.5, 0.5]
        for i in range(self.N_agents):
            agent = Trader(id=i, investorType=random.choices(investor_type, investor_type_probabilities)[0])
            agents[i] = agent
        return agents

    def market_interactions(self):
        white_noise = random.uniform(-1, 1)
        for id, agent in self.agents.items():
            agent.decision_based_on_personal_strategy(self.market_environment.current_price,
                                                      self.market_environment.price_history, white_noise)
        self.market_environment.update_market(self.agents)

    def run_simulation(self):
        trading_day = 0
        for i in range(self.time_steps):
            self.market_interactions()
            trading_day += 1


def setup_env(ticker, start_date_history, end_date_history, time_steps, N_agents):
    ticker = yf.Ticker(ticker)
    price_history = get_price_history(ticker, start_date=start_date_history, end_date=end_date_history)
    price_history = select_closing_prices(price_history)
    last_price = price_history[-1]
    market_environment = MarketEnvironment(initial_price=last_price, name="Test Market",
                                           start_date=datetime.datetime.strptime(end_date_history, "%Y-%m-%d"), price_history=price_history)
    simulation = SimulationClass(time_steps=time_steps, N_agents=N_agents, market_environment=market_environment)
    return simulation


if __name__ == '__main__':
    simulation = setup_env("AAPL", "2020-11-15", "2020-12-15", 1000, 5000)
    simulation.run_simulation()
