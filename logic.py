import networkx as nx
from objects import *


class Graph_countries(nx.Graph):

    def __init__(self):
        super().__init__()
        self.initialization()

    def initialization(self):
        for country in Country.countries:
            self.add_node(country.name)
        for country in Country.countries:
            if len(country.deal) > 0:
                for other_country in country.deal:
                    self.add_edge(country.name, other_country.name)


graph = Graph_countries()
# graph.initialization()
