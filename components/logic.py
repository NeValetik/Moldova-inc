import networkx as nx
from objects import *


def new_game():
    directory = "components/resume"
    files = os.listdir(directory)

    # Iterate over each file and remove it
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):  # Check if it's a file
            os.remove(file_path)


def exit_game():
    with open("components/resume/x.txt", "w") as input:
        for line in graph.x:
            input.write(line)
            input.write("\n")

    with open("components/resume/y.txt", "w") as input:
        for line in graph.y:
            input.write(str(int(line)))
            input.write("\n")

    with open("components/resume/winedata.txt", "w") as input:
        input.write(str(BarsGetters.get_wine_advertisment()))
        input.write("\n")
        input.write(str(BarsGetters.get_wine_naturality()))
        input.write("\n")
        input.write(str(BarsGetters.get_wine_taste()))
        input.write("\n")

    with open("components/resume/graph.txt", "w") as input:
        for u, v in graph.edges():
            input.write(v.name.replace(" ", "-") + ' ' + str(v.end_year) + ' ' + str(v.contracted) + "\n")
    sys.exit()


def xinit():
    try:
        with open("components/resume/x.txt", "r") as input:
            x = []
            for line in input.readlines():
                if line != '\n':
                    x.append(line[:-1])

            return x

    except:
        return []


def yinit():
    try:
        with open("components/resume/y.txt", "r") as input:
            x = []

            for line in input.readlines():
                print(line)
                if line != '\n':
                    x.append(int(line[:-1]))
            return x
    except:
        print("New game apparently...")
        return []


def total_income_init():
    try:
        with open("components/resume/y.txt", "r") as input:
            return int(input.readlines()[-1][:-1])
    except:
        return 90_000


def countries_init():
    try:
        print("Inside countryis init")
        countries = []
        with open("components/resume/graph.txt", "r") as input:
            print(input)
            for line in input:
                parts = [part.strip() for part in line.split()]
                print(parts)
                if len(parts) == 3:
                    countryin = parts[0].replace("-", " ")
                    number = float(parts[1])
                    status = bool(parts[2])
                countries.append((countryin, number, status))
            print(countries)
            return countries

    except:
        print("This except")
        return []


class Graph(nx.Graph):
    initiated = False
    total_income = total_income_init()
    countries_init = countries_init()
    x = xinit()
    y = yinit()

    checked_txt = False

    def __init__(self):
        super().__init__()

        for country in Country.countries:
            self.add_node(country.name)

    def update(self):
        # self.check_contracts_data_base()
        self.check_new_contracts()
        self.check_data_contracts()
        self.collect_data_for_statistics_week()

    def check_new_contracts(self):
        # print(Country.countries)
        self.check_remove_invalid_by_date_contract()
        while len(Country.contracts) != 0:
            contract = Country.contracts[0]
            weight = self.income(contract[1])
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
                    country.contracted = self.countries_init[0][1]
                    country.end_year = self.countries_init[0][2]
                    self.add_weighted_edges_from([(country.moldova, country, 0)])
                    self.countries_init.pop(0)

    def income(self, contract):
        return Wine.naturality * contract.naturality_coef + Wine.advertisment * contract.advertisment_coef + Wine.taste * contract.taste_coef

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
        if len(self.x) < 52 and Timer.get_time() not in self.x:
            self.x.append(Timer.get_time())
            self.y.append(self.total_income)
            # print(self.y)

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
