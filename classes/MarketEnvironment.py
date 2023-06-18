import random

import matplotlib.pyplot as plt


class MarketEnvironment:
    """
    Artificial market environment where prices are getting updated according to agent excess demand
    """
    def __init__(self, initial_price, name, price_history, start_date):
        self.name = name
        self.initial_price = initial_price
        self.current_price = initial_price
        self.excess_demand = 0
        self.tau = 0.9
        self.price_history = price_history
        self.date = start_date

    def update_market(self, agents):
        self.price_history.append(self.current_price)
        self.update_excess_demand(agents)
        updated_price = self.current_price + self.tau * self.excess_demand
        if updated_price < 0:
            updated_price - random.uniform(0, 0.05)
        self.current_price = updated_price
        print("Updated Price: ", self.current_price)
        return updated_price

    def update_excess_demand(self, traders):
        demand = 0
        for id, trader in traders.items():
            demand += trader.demand
        normalized_demand = demand / len(traders)
        self.excess_demand = normalized_demand
        return normalized_demand

    def plot_price_history(self):
        plt.figure(figsize=(10, 10))
        plt.plot([i for i in range(len(self.price_history))], self.price_history, 'r--', label='Simulation values')
        max_price = [max(self.price_history)] * len(self.price_history)
        min_price = [min(self.price_history)] * len(self.price_history)
        plt.plot(max_price, 'g--', label='Max Price')
        plt.plot(min_price, 'b--', label='Min Price')
        plt.xlabel('Simulation step', fontsize=14, )
        plt.ylabel('Price', fontsize=14)
        plt.title('Price evolution', fontsize=16)
        plt.legend(loc='upper right')
        plt.show()