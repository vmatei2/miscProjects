import random

from classes.InvestorTypes import InvestorTypes


class Trader():
    def __init__(self, id, investorType=None):
        self.demand = 0
        self.b = random.uniform(-1, 1)  # gives the strength of the force calculated as simply (current price - moving_average)
        self.fundamental_price = random.randint(115, 120)
        self.id = id
        self.investorType = investorType

    def decision_based_on_personal_strategy(self, current_price, price_history, white_noise):
        if self.investorType == InvestorTypes.LONGTERM:
            expected_price = self.compute_price_expectation_fundamentalist(current_price, price_history, white_noise)
        else:
            expected_price = self.compute_price_expectation_chartist(current_price, price_history, white_noise)
        self.update_demand(expected_price, current_price)

    def update_demand(self, expected_price, current_price):
        if expected_price > current_price:
            self.demand += 0.01
        elif expected_price == current_price:
            pass
        else:
            self.demand -= 0.01

    def compute_price_expectation_chartist(self, current_price, price_history, white_noise):
        """
        Insipred from - minimal agent based model for financial markets
        Chartists agents detect a trend through looking at the distance between the price and its smoothed profile (
        given by moving average in this case) :param current_price: :param current_trading_day: :param price_history:
        :param white_noise: :return:
        """
        # below if statement considers whether the agent is simply looking for a quick profit, get in-get out or
        # believe in GME
        rolling_average_window_length = 5
        rolling_average = self.compute_rolling_average(price_history, rolling_average_window_length)
        expected_price = current_price + self.b * (current_price - rolling_average) + white_noise
        self.expected_price = expected_price
        return expected_price

    def compute_rolling_average(self, price_history, rolling_average_window_length):
        total_prices = 0
        price_history = price_history[-rolling_average_window_length:]
        for i in range(rolling_average_window_length):
            total_prices += price_history[i]
        rolling_average = total_prices / rolling_average_window_length
        return rolling_average

    def compute_price_expectation_fundamentalist(self, current_price, price_history, white_noise):
        """
        Inspired from - mininal agent based model for financial markets
        Long-term view agents are modelled through a stochastic equation written in terms of a random walk
        :param current_price:
        :param price_history:
        :param white_noise:
        :return:
        """
        expected_price = current_price + abs(self.b) * (self.fundamental_price - current_price) + white_noise
        return expected_price