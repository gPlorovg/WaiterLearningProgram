from random import choice, sample
from db_manage import db


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
            resp = sample([i for i in db.read_all_volumes(table) if i != true_ans], count)
        case "serving":
            resp = sample([i for i in db.read_all_serving(table) if i and i != true_ans], count)
        case "ingredients":
            resp = sample([i for i in db.read_all_ingredients(table) if i not in true_ans], count)

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


def generate_exam(section: str) -> tuple:
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
                while not obj.serving:
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
            "wrong_ingredients": get_wrong_ans("cocktails", "ingredients", obj.ingredients, 4),
            "img_path": obj.img_path
        }

    return state, resp


def match_quiz(section: str, type_: str, count: int) -> tuple:
    obj_list = list()
    resp = list()
    state = "Error"

    match section:
        case "bar":
            id_list = sample(db.all_drinks_id, count)
            obj_list = map(db.read_drink, id_list)
        case "cocktails":
            id_list = sample(db.all_cocktails_id, count)
            obj_list = map(db.read_cocktail, id_list)
        case "menu":
            id_list = sample(db.all_meals_id, count)
            obj_list = map(db.read_meal, id_list)

    if obj_list:
        state = "Success"
        match type_:
            case "price":
                for obj in obj_list:
                    resp.append({
                        "id": obj.id,
                        "name": obj.name,
                        "price": obj.price
                    })
            case "volume":
                for obj in obj_list:
                    resp.append({
                        "id": obj.id,
                        "name": obj.name,
                        "volume": obj.volume
                    })
            case "serving":
                for obj in obj_list:
                    resp.append({
                        "id": obj.id,
                        "name": obj.name,
                        "serving": obj.serving
                    })

    return state, resp


state, exam_bar_data = generate_exam("bar")
if state != "Success":
    assert Exception

state, exam_cocktails_data = generate_exam("cocktails")
if state != "Success":
    assert Exception

state, exam_menu_data = generate_exam("menu")
if state != "Success":
    assert Exception
