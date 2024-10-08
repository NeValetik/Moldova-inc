import networkx as nx
from objects import *


def new_game():
    directory = "components/saved_game"
    files = os.listdir(directory)

    # Iterate over each file and remove it
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):  # Check if it's a file
            os.remove(file_path)


def exit_game():
    with open("components/saved_game/x.txt", "w") as input:
        for line in graph.x:
            input.write(line)
            input.write("\n")

    with open("components/saved_game/y.txt", "w") as input:
        for line in graph.y:
            input.write(str(int(line)))
            input.write("\n")

    with open("components/saved_game/winedata.csv", "w") as input:
        input.write("advertisment,advertisment_index,naturality,naturality_index,taste,taste_index,trademark,total_accumulated\n")
        for wine in Wine.wines:
            input.write(str(BarsGetters.get_wine_advertisment(wine))+","+str(wine.advertisment_index)+","+str(BarsGetters.get_wine_naturality(wine))+","+str(wine.naturality_index)+","+str(BarsGetters.get_wine_taste(wine))+","+str(wine.taste_index)+","+str(wine.name)+","+str(int(wine.total_accumulated))+"\n")
            #advertisment,advertisment_index,naturality,naturality_index,taste,taste_index,trademark
            #10000,-1,10000,-1,10000,-1,white-wine
    with open("components/saved_game/graph.txt", "w") as input:
        for u, v in graph.edges():
            input.write(v.name.replace(" ", "-") + ' ' + str(v.end_year) + ' ' + str(v.contracted) + "\n")

    with open("components/saved_game/stored_news.csv", "w") as input:
        input.write("id,event,date,news,naturality_bonus,taste_bonus,advertisment_bonus\n")
        NewsItem.store_notification()
        for news in NewsItem.stored_notifications:
            input.write(str(news.id)+","+str(news.event)+","+str(news.date)+","+str(news.news)+","+str(news.naturality_bonus)+","+str(news.taste_bonus)+","+str(news.advertisment_bonus)+"\n")

    with open("components/saved_game/taxes.csv", "w") as input:
        input.write("taxes_payed,taxes_sum\n")
        input.write(str(Graph.taxes_payed) + ',' + str(Graph.taxes_sum) + "\n") 

    sys.exit()


class GraphInit:
    @classmethod
    def _initialize(cls):
        cls.total_income_init()
        cls.countries_init()
        cls.xinit()
        cls.yinit()
        cls.taxes_load()
    
    
    def xinit():
        try:
            with open("components/saved_game/x.txt", "r") as input:
                x = []
                for line in input.readlines():
                    if line != '\n':
                        x.append(line[:-1])

                Graph.x = x

        except:
            Graph.x = []


    def yinit():
        try:
            with open("components/saved_game/y.txt", "r") as input:
                x = []

                for line in input.readlines():
                    # print(line)
                    if line != '\n':
                        x.append(int(line[:-1]))
                Graph.y = x
        except:
            print("New game apparently...")
            Graph.y = []


    def total_income_init():
        try:
            with open("components/saved_game/y.txt", "r") as input:
                Graph.total_income = int(input.readlines()[-1][:-1])
        except:
            Graph.total_income = 90_000


    def countries_init():
        try:
            countries = []
            with open("components/saved_game/graph.txt", "r") as input:
                for line in input:
                    parts = [part.strip() for part in line.split()]
                    # print(parts)
                    if len(parts) == 3:
                        countryin = parts[0].replace("-", " ")
                        number = float(parts[1])
                        status = bool(parts[2])
                    countries.append((countryin, number, status))
                Graph.countries_init = countries

        except:
            print("This except")
            Graph.countries_init = []

    def taxes_load():        
        try:
            with open("components/saved_game/taxes.csv", "r") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    Graph.taxes_payed = float(row["taxes_payed"])
                    Graph.taxes_sum = float(row["taxes_sum"])
        except:
            pass

class Graph(nx.Graph):
    initiated = False
    total_income = 900_000
    countries_init = []
    x = []
    y = []
    taxes_payed = 0 #holds the year from the begining for which the taxes was payed including the years before
    taxes_sum = 1000

    def __init__(self):
        super().__init__()
        for country in Country.countries:
            self.add_node(country.name)

    def update(self):
        # self.check_contracts_data_base()
        self.check_new_contracts()
        self.check_data_contracts()
        self.collect_data_for_statistics_week()
        self.count_the_taxes()

    def check_new_contracts(self):
        # print(Country.countries)
        self.check_remove_invalid_by_date_contract()
        while len(Country.contracts) != 0:
            contract = Country.contracts[0]
            weight = income(contract[1])
            Graph.total_income += weight
            self.add_weighted_edges_from([(contract[0], contract[1], weight)])
            del Country.contracts[0]
        self.checked_txt = True
        # print(Country.countries)

    def check_data_contracts(self):
        if len(self.countries_init) != 0:
            # print(self.countries_init)
            for country in Country.countries:
                if len(self.countries_init) != 0 and self.countries_init[0][0] == country.name:
                    country.contracted = self.countries_init[0][2]
                    country.end_year = self.countries_init[0][1]
                    self.add_weighted_edges_from([(country.moldova, country, 0)])
                    self.countries_init.pop(0)

    def check_remove_invalid_by_date_contract(self):
        for u, v in self.edges():
            if v.end_year < Timer.get_initial_time_in_years():
                # print(v.contracted)
                v.contracted = False
                self.remove_edge(u, v)

    def get_total_income(self):
        temp_sum = 0
        for u, v, d in self.edges(data=True):
            temp_sum += d['weight']
        # print(temp_sum)    
        return temp_sum

    def collect_data_for_statistics_week(self):
        if len(self.x) < 24 and Timer.get_time() not in self.x:
            self.x.append(Timer.get_time())
            self.y.append(self.total_income)
            # print(self.y)

        elif Timer.get_time() not in self.x:
            self.x.pop(0)
            self.x.append(Timer.get_time())
            self.y.pop(0)
            self.y.append(self.total_income)

    def count_the_taxes(self):
        if Graph.taxes_payed != int(Timer.get_initial_time_in_years()):
            Graph.taxes_payed = int(Timer.get_initial_time_in_years())
            Graph.total_income -= (Graph.taxes_sum*Graph.taxes_payed+0.1*Graph.total_income)

graph = Graph()


class BarsGetters:

    @staticmethod
    def get_world_progress():
        return Graph.total_income

    @staticmethod
    def get_wine_naturality(wine):
        return wine.naturality

    @staticmethod
    def get_wine_advertisment(wine):
        return wine.advertisment

    @staticmethod
    def get_wine_taste(wine):
        return wine.taste
