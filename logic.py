import networkx as nx
from objects import *


class Graph_countries(nx.Graph):
    # print(countries)
    # countries = [{"name":"USA","deal": ["Moldova"]},{"name":"Russia/Ukraina","deal": ["Moldova"]},
                #  {"name":"Arabian","deal": []},{"name":"Africa","deal": []},{"name":"Moldova","deal": []}]


    def initialization(self):
        for i in Country.countries:
            self.add_node(i.name)
        for i in Country.countries:
            if len(i.deal)>0:
                self.add_edge(i.name,i.deal[0])


graph = Graph_countries()
graph.initialization()
