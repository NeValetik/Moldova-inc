import csv

# time = input().split('/')
# time = [int(t) for t in time]
# calculate = time[2]+time[1]/12+time[0]/365
# print(calculate)


with open("components/saved_game/stored_news.csv") as saved_file:
    csv_saved_reader = csv.DictReader(saved_file)
    for r in csv_saved_reader:
        print(r)