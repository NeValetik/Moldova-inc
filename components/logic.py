import networkx as nx
from objects import *


class Graph(nx.Graph):
    initiated = False

    def __init__(self):
        super().__init__()
        self.initialization()

    def initialization(self):
        for country in Country.countries:
            self.add_node(country.name)

    def check_new_contracts(self):
        while len(Country.contracts) != 0:
            contract = Country.contracts[0]
            self.add_edge(contract[0], contract[1])
            del Country.contracts[0]


graph = Graph()


class Market:

    w1 = Wine("Freedom Blend")
    w1.set_taste(5)
    w1.set_naturality(10)
    w1.set_naturality(100)
    w2 = Wine("Castel Mimi", 1, 2,3)



    @staticmethod
    def get_total_profit(self):
        return self.w1.calculate_total_profit()


class BarsGetters:

    @staticmethod
    def get_world_progress():
        return Market.get_total_profit()
