import networkx as nx
from objects import *
from scenes import *
from scenes import UpgradeMenu

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
            weight = self.formula(contract[1])
            self.add_weighted_edges_from([(contract[0], contract[1], weight)])
            del Country.contracts[0]
        self.check_new_value_formula()    
    

    def check_new_value_formula(self):
        print(UpgradeMenu.get_naturality())
        for u,v,d in self.edges(data=True):
            d['weight'] = self.formula(v)
            print("Nodes: ",u.name," ", v.name ,"Weightened edges: ",d)

    
    def formula(self,contract):
        return UpgradeMenu.get_naturality() * contract.naturality_coef + UpgradeMenu.get_advertisment() * contract.advertisment_coef + UpgradeMenu.get_taste() * contract.taste_coef


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
