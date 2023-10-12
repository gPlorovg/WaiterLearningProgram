from os import getenv
from random import choice, sample
from dotenv import load_dotenv
from db_manage import DataBase


load_dotenv()
USER = getenv("USER")
HOST = getenv("HOST")
DB_PASSWORD = getenv("DB_PASSWORD")

db = DataBase("WaiterLearningProgram_db", USER, HOST, DB_PASSWORD)


def get_wrong_ans(section: str, type_: str, true_ans, count: int) -> list:
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
            resp = sample([i for i in db.read_all_prices(table) if i != true_ans], count)
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
            "wrong_prices": get_wrong_ans(section, "price", obj.price, 3)
        }

    return state, resp


def exam(section: str) -> tuple:
    resp = list()
    state = "Error"

    match section:
        case "bar":
            for id_ in db.all_drinks_id:
                obj = db.read_drink(id_)
                resp.append({
                    "id": id_,
                    "section": obj.section,
                    "name": obj.name,
                    "price": obj.price,
                    "volume": obj.volume,
                    "wrong_volumes": get_wrong_ans(section, "volume", obj.volume, 3),
                    "serving": obj.serving,
                    "wrong_serving": get_wrong_ans(section, "serving", obj.serving, 3)
                })
        case "cocktails":
            for id_ in db.all_cocktails_id:
                obj = db.read_cocktail(id_)
                resp.append({
                    "id": id_,
                    "section": obj.section,
                    "name": obj.name,
                    "img_path": obj.img_path,
                    "price": obj.price,
                    "ingredients": obj.ingredients,
                    "wrong_ingredients": get_wrong_ans(section, "ingredients", obj.ingredients, 3)
                })
        case "menu":
            for id_ in db.all_meals_id:
                obj = db.read_meal(id_)
                resp.append({
                    "id": id_,
                    "section": obj.section,
                    "name": obj.name,
                    "description": obj.description,
                    "price": obj.price,
                    "serving": obj.serving,
                    "wrong_serving": get_wrong_ans(section, "serving", obj.serving, 3)
                })

    if resp:
        state = "Success"

    return state, resp


def mistakes(section: str, mistakes_id: list) -> tuple:
    resp = list()
    state = "Error"

    match section:
        case "bar":
            for id_ in mistakes_id:
                obj = db.read_drink(id_)
                resp.append({
                    "id": id_,
                    "section": obj.section,
                    "name": obj.name,
                    "price": obj.price,
                    "volume": obj.volume,
                    "wrong_volumes": get_wrong_ans(section, "volume", obj.volume, 3),
                    "serving": obj.serving,
                    "wrong_serving": get_wrong_ans(section, "serving", obj.serving, 3)
                })
        case "cocktails":
            for id_ in mistakes_id:
                obj = db.read_cocktail(id_)
                resp.append({
                    "id": id_,
                    "section": obj.section,
                    "name": obj.name,
                    "img_path": obj.img_path,
                    "price": obj.price,
                    "ingredients": obj.ingredients,
                    "wrong_ingredients": get_wrong_ans(section, "ingredients", obj.ingredients, 3)
                })
        case "menu":
            for id_ in mistakes_id:
                obj = db.read_meal(id_)
                resp.append({
                    "id": id_,
                    "section": obj.section,
                    "name": obj.name,
                    "description": obj.description,
                    "price": obj.price,
                    "serving": obj.serving,
                    "wrong_serving": get_wrong_ans(section, "serving", obj.serving, 3)
                })

    if resp:
        state = "Success"

    return state, resp


def guess_serving(section: str) -> tuple:
    id_ = 0
    obj = None
    resp = dict()
    state = "Error"

    match section:
        case "bar":
            id_ = choice(db.all_drinks_id)
            obj = db.read_drink(id_)
        case "menu":
            id_ = choice(db.all_meals_id)
            obj = db.read_meal(id_)

    if obj:
        state = "Success"
        resp = {
            "id": id_,
            "section": obj.section,
            "name": obj.name,
            "serving": obj.serving,
            "wrong_serving": get_wrong_ans(section, "serving", obj.serving, 3)
        }

    return state, resp


def guess_ingredients() -> tuple:
    resp = dict()
    state = "Error"

    id_ = choice(db.all_cocktails_id)
    obj = db.read_cocktail(id_)

    if obj:
        state = "Success"
        resp = {
            "id": id_,
            "section": obj.section,
            "name": obj.name,
            "ingredients": obj.ingredients,
            "wrong_ingredients": get_wrong_ans("cocktails", "ingredients", obj.ingredients, 4)
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
