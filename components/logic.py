import networkx as nx
from objects import *

class Graph(nx.Graph):
    initiated = False
    total_income = 90_000

    def __init__(self):
        super().__init__()
        
        for country in Country.countries:
            self.add_node(country.name)

    def update(self):
        self.check_new_contracts()

    def check_new_contracts(self):
        while len(Country.contracts) != 0:
            contract = Country.contracts[0]
            weight = self.income(contract[1])
            Graph.total_income += weight
            self.add_weighted_edges_from([(contract[0], contract[1], weight)])
            del Country.contracts[0]

    def income(self,contract):
        return Wine.naturality * contract.naturality_coef + Wine.advertisment * contract.advertisment_coef + Wine.taste * contract.taste_coef


graph = Graph()

# This class is unutilized, so I decided to comment it out
'''
class Market:

    w1 = Wine("Freedom Blend")
    w1.set_taste(5)
    w1.set_naturality(10)
    w1.set_naturality(100)
    w2 = Wine("Castel Mimi", 1, 2,3)



    @staticmethod
    def get_total_profit(self):
        return self.w1.calculate_total_profit()
'''

class BarsGetters:

    @staticmethod
    def get_world_progress():
        return Graph.total_income
    
    @staticmethod
    def get_wine_naturality():
        return Wine.naturality
    
    @staticmethod
    def get_wine_advertisment():
        return Wine.advertisment
    
    @staticmethod
    def get_wine_taste():
        return Wine.taste
