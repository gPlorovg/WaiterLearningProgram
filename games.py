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


def get_wrong_ans(section: str, type_: str) -> list:
    resp = list()
    table = None

    match section:
        case "bar":
            table = "drinks"
        case "cocktails":
            table = "cocktails"
        case "menu":
            table = "meals"

    match type_:
        case "price":
            resp = sample(db.read_all_prices(table), 3)
        case "volume":
            pass
        case "serving":
            pass
        case "ingredients":
            pass

    return resp


def guess_price(section: str) -> tuple:
    id_ = 0
    obj = None
    resp = dict()
    state = "Error"

    match section:
        case "bar":
            id_ = choice(db.all_drinks_id)
            obj = db.read_drink(id_)
        case "cocktails":
            id_ = choice(db.all_cocktails_id)
            obj = db.read_cocktail(id_)
        case "menu":
            id_ = choice(db.all_meals_id)
            obj = db.read_meal(id_)
    if obj:
        state = "Success"
        resp = {
            "id": id_,
            "section": obj.section,
            "name": obj.name,
            "price": obj.price,
            "wrong_ans": get_wrong_ans(section, "price")
        }

    return state, resp


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
