import networkx as nx
from objects import *
# from scenes import *

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
            weight = self.income(contract[1])
            self.add_weighted_edges_from([(contract[0], contract[1], weight)])
            del Country.contracts[0]
        self.check_new_value_formula()    
    
    def check_new_value_formula(self):
        for u,v,d in self.edges(data=True):
            d['weight'] = self.income(v)
            print("Nodes: ",u.name," ", v.name ,"Weightened edges: ",d)

    def income(self,contract):
        return Wine.naturality * contract.naturality_coef + Wine.advertisment * contract.advertisment_coef + Wine.taste * contract.taste_coef

    def get_total_income(self):
        temp_sum = 0
        for u,v,d in self.edges(data=True):
            temp_sum += d['weight']
        return temp_sum    

graph = Graph()

#This class is unutilized, so I decided to comment it out
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
        return graph.get_total_income()
