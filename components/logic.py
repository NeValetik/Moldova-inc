import networkx as nx
from objects import *

class Graph(nx.Graph):
    initiated = False
    total_income = 90_000
    x=[]
    y=[]

    def __init__(self):
        super().__init__()
        
        for country in Country.countries:
            self.add_node(country.name)

    def update(self):
        self.check_new_contracts()
        self.collect_data_for_statistics_week()

    def check_new_contracts(self):
        self.check_remove_invalid_by_date_contract()
        while len(Country.contracts) != 0:
            contract = Country.contracts[0]
            weight = self.income(contract[1])
            Graph.total_income += weight
            self.add_weighted_edges_from([(contract[0], contract[1], weight)])
            del Country.contracts[0]

    def income(self,contract):
        return Wine.naturality * contract.naturality_coef + Wine.advertisment * contract.advertisment_coef + Wine.taste * contract.taste_coef

    def check_remove_invalid_by_date_contract(self):
        for u,v in self.edges():
            if v.end_year < Timer.get_time_in_years():
                # print(v.contracted)
                v.contracted = False
                self.remove_edge(u,v)

    def get_total_income(self):
        temp_sum = 0
        for u,v,d in self.edges(data=True):
            temp_sum += d['weight']
        # print(temp_sum)    
        return temp_sum

    def collect_data_for_statistics_week(self):    
        if len(self.x)<52 and Timer.get_time() not in self.x:
            self.x.append(Timer.get_time())
            self.y.append(self.total_income)
        elif Timer.get_time() not in self.x:
            self.x.pop(0)
            self.x.append(Timer.get_time())
            self.y.pop(0)
            self.y.append(self.total_income)

graph = Graph()


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
