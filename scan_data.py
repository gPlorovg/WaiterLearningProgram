import csv
from os import listdir
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
                meals_list.append(Meal(name=name, section=section, price=price, serving=serving,
                                       description=description))
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
        meals_list.append(Meal(name=row[0], section=section, price=price, serving=serving, description=description))

drink_list = list()
with open("data/drinks.csv") as f:
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        if row[0]:
            if row[3] == "Цена":
                section = row[0]
                section_ = section
            else:
                if section != "КОКТЕЙЛИ/COCKTAILS":
                    if row[4]:
                        serving = row[4].replace('\n', " ")
                    if row[1] == "":
                        section_ = section + " | " + row[0]
                    else:
                        name = row[0].split("/")[0]
                        price = int(row[3].rstrip("р.").replace(" ", ""))
                        volume = float(row[1].replace(",", "."))
                        if volume < 1:
                            volume *= 1000
                        volume = int(volume)
                        drink_list.append(Drink(name=name, section=section, price=price, serving=serving, volume=volume))

imgs = listdir("data/cocktail_img")
cocktail_list = list()
with open("data/cocktails.csv") as f:
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        if row[0]:
            if not row[1]:
                section = row[0]
            else:
                name = row[0]
                ingredients = [i.rstrip().lstrip() for i in row[1].split(" | ")]
                serving = row[3]
                volume = int(row[4].rstrip(" мл"))
                price = int(row[5].rstrip(" р."))
                img_path = "data/cocktail_img/" + imgs.pop(0)
                cocktail_list.append(Cocktail(name=name, section=section, price=price, serving=serving,
                                              ingredients=ingredients, img_path=img_path, volume=volume))
