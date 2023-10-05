from os import getenv
from random import choice, sample
from dotenv import load_dotenv
from db_manage import DataBase


load_dotenv()
USER = getenv("USER")
HOST = getenv("HOST")
DB_PASSWORD = getenv("DB_PASSWORD")

db = DataBase("WaiterLearningProgram_db", USER, HOST, DB_PASSWORD)


# name, price, serving, volume
def exam_drinks() -> dict:
    pass


def exam_cocktails() -> dict:
    pass


def exam_meals() -> dict:
    pass


def guess_price(is_meal: bool) -> tuple:
    if is_meal:
        name = choice(db.all_meals)
        meal = db.read_meal(name)
        price = meal.price
    else:
        name = choice(db.all_drinks)
        drink = db.read_drink(name)
        price = drink.price

    return name, price


def match_prices(is_meal: bool) -> dict:
    resp = dict()

    if is_meal:
        names = sample(db.all_meals, 6)
        for name in names:
            resp[name] = db.read_meal(name).price
    else:
        names = sample(db.all_drinks, 6)
        for name in names:
            resp[name] = db.read_drink(name).price

    return resp


def build_recipe(is_meal: bool) -> tuple:
    if is_meal:
        name = choice(db.all_meals)
        meal = db.read_meal(name)
        right_ingredients = meal.ingredients
        wrong_ingredients = list()
        i = 0

        while len(wrong_ingredients) < 4:
            if i < len(meal.alternatives):
                wrong_ingredients += list(set(db.read_meal(meal.alternatives[i]).ingredients) - set(right_ingredients)
                                          - set(wrong_ingredients))
                i += 1
            else:
                add_name = choice(db.all_meals)
                while add_name == name:
                    add_name = choice(db.all_meals)
                wrong_ingredients += list(set(db.read_meal(add_name).ingredients) - set(right_ingredients)
                                          - set(wrong_ingredients))
    else:
        name = choice(db.all_drinks)
        drink = db.read_drink(name)
        right_ingredients = drink.ingredients
        wrong_ingredients = list()
        i = 0

        while len(wrong_ingredients) < 4:
            if i < len(drink.alternatives):
                wrong_ingredients += list(set(db.read_drink(drink.alternatives[i]).ingredients) - set(right_ingredients)
                                          - set(wrong_ingredients))
                i += 1
            else:
                add_name = choice(db.all_drinks)
                while add_name == name:
                    add_name = choice(db.all_drinks)
                wrong_ingredients += list(set(db.read_drink(add_name).ingredients) - set(right_ingredients)
                                          - set(wrong_ingredients))

    return right_ingredients, sample(wrong_ingredients, 4)
