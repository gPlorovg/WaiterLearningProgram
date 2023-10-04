import csv
from Objects import Meal, Drink, Cocktail


meals_list = list()
with open("data/Meals.csv") as f:
    reader = csv.reader(f, delimiter=";")
    count_of_obj_rows = 0
    for row in reader:
        if row[0] or row[1]:
            if len(row[0]) > 3:
                section = row[0]
            else:
                if count_of_obj_rows == 0:
                    name = row[1]
                    price = int(row[2].split()[0])
                    count_of_obj_rows = 1
                elif count_of_obj_rows == 1:
                    description = row[1]
                    count_of_obj_rows = 2
                elif count_of_obj_rows == 2:
                    serving = row[1].lstrip("Сервировка: ")
                    count_of_obj_rows = 3
            if count_of_obj_rows == 3:
                meals_list.append(Meal(name, section, price, serving, description))
                count_of_obj_rows = 0
with open("data/Meals_add.csv") as f:
    reader = csv.reader(f, delimiter=";")
    section = "Гарниры"
    price = 250
    serving = ""
    description = ""
    for row in reader:
        if row[0] == "Сырный":
            section = "Соуса"
            price = 100
        if len(row) > 1:
            description = row[1]
        else:
            description = ""
        meals_list.append(Meal(row[0], section, price, serving, description))
drink_list = list()

