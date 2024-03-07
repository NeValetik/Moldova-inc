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

class BarsGetters:
    @staticmethod
    def get_world_progress():
        return 69
    