# import json
# from os import getenv
from random import shuffle
# from dotenv import load_dotenv
from flask import Flask, render_template, make_response, request
# from db_manage import db
# from Objects import User
import games


# load_dotenv()
# USER = getenv("USER")
# HOST = getenv("HOST")
# DB_PASSWORD = getenv("DB_PASSWORD")

app = Flask(__name__)


# STATUS CODES: 200 - user not in db, 409- user already exists, 500- req_db error, 503 - db doesn't connected
# 401 - user doesn't exist
# @app.route("/")
# def index():  # put application's code here
#     return render_template("index.html")


# @app.route("/sign_up", methods=["GET", "POST"])
# def sign_up():
#     if request.method == "GET":
#         return render_template("sign_up.html")
#     elif request.method == "POST":
#         req = request.json
#         check_resp = db.check_user(req["email"])
#         if check_resp[1] == 200:
#             resp = db.create_user(User(email=req["email"], name=req["name"], password=req["password"]))
#             if resp[1] == 200:
#                 db.commit()
#         else:
#             resp = check_resp
#         return make_response(resp)


# @app.post("/sign_in")
# def sign_in():
#     req = request.json
#     resp = db.sign_in(name_=req["name"], password_=req["password"])
#     return make_response(resp)


# @app.get("/main")
@app.get("/")
def main():
    return render_template("main.html")


@app.get("/bar")
@app.get("/cocktails")
@app.get("/menu")
def quizzies_list():
    # mistakes_count = int(request.args.get("mistakes_count"))
    names = list()
    if request.path == "/bar":
        names = ["guess_serving", "match_price", "match_volume"]
    elif request.path == "/cocktails":
        names = ["guess_ingredients", "match_price"]
    elif request.path == "/menu":
        names = ["guess_serving", "match_price"]
    title = request.path.lstrip("/")
    title = title[0].upper() + title[1:]
    return render_template("quizzies_list.html", title=title, names=names)


@app.get("/bar/guess_price")
@app.get("/cocktails/guess_price")
@app.get("/menu/guess_price")
def guess_price():
    section = request.path.split("/")[1]
    state, data = games.guess_price(section)

    # i = 0
    # while state != "Success" and i < 3:
        # db.refresh_conn("WaiterLearningProgram_db", "WaiterLearningProgram", HOST, DB_PASSWORD)
        # state, data = games.guess_price(section)
        # i += 1

    prices = data["wrong_prices"]
    prices.append(data["price"])
    shuffle(prices)
    if state == "Success":
        return render_template("guess_price.html", title="guess_price", section=data["section"], name=data["name"],
                               prices=prices, true_ans=data["price"])
    else:
        return make_response(state, 500)


@app.template_filter("short_value")
def short_value(s: str) -> str:
    return s[:10] + str(len(s))


@app.get("/bar/guess_serving")
@app.get("/menu/guess_serving")
def guess_serving():
    section = request.path.split("/")[1]
    state, data = games.guess_serving(section)

    # i = 0
    # while state != "Success" and i < 3:
        # db.refresh_conn("WaiterLearningProgram_db", "WaiterLearningProgram", HOST, DB_PASSWORD)
        # state, data = games.guess_serving(section)
        # i += 1

    serving = data["wrong_serving"]
    serving.append(data["serving"])
    shuffle(serving)
    if state == "Success":
        return render_template("guess_serving.html", title="guess_serving", section=data["section"], name=data["name"],
                               serving=serving, true_ans=short_value(data["serving"]))
    else:
        return make_response(state, 500)


@app.get("/cocktails/guess_ingredients")
def guess_ingredients():
    state, data = games.guess_ingredients()
    print(data)
    # i = 0
    # while state != "Success" and i < 3:
        # db.refresh_conn("WaiterLearningProgram_db", "WaiterLearningProgram", HOST, DB_PASSWORD)
        # state, data = games.guess_ingredients()
        # i += 1

    ingredients = data["wrong_ingredients"] + data["ingredients"]
    shuffle(ingredients)
    if state == "Success":
        return render_template("guess_ingredients.html", title="guess_ingredients", section=data["section"],
                               name=data["name"], ingredients=ingredients, true_ans=data["ingredients"],
                               img_path=data["img_path"])
    else:
        return make_response(state, 500)


@app.get("/bar/match_price")
@app.get("/cocktails/match_price")
@app.get("/menu/match_price")
@app.get("/bar/match_volume")
@app.get("/cocktails/match_volume")
@app.get("/menu/match_volume")
def match_quiz():
    section = request.path.split("/")[1]
    type_ = request.path.split("_")[1]
    state, data = games.match_quiz(section, type_, 4)

    # i = 0
    # while state != "Success" and i < 3:
        # db.refresh_conn("WaiterLearningProgram_db", "WaiterLearningProgram", HOST, DB_PASSWORD)
        # state, data = games.match_quiz(section, type_, 4)
        # i += 1

    names = list(map(lambda x: x["name"], data))
    sections = list(map(lambda x: x["section"], data))
    for i in range(len(names)):
        names[i] = sections[i] + " || " + names[i]

    qualities = list(map(lambda x: x[type_], data))
    shuffle(qualities)
    items = {names[i]: qualities[i] for i in range(len(names))}
    template_name = "match_" + type_ + ".html"
    if state == "Success":
        return render_template(template_name, title="match_" + type_, items=items, true_ans=data, type=type_)
    else:
        return make_response(state, 500)


@app.get("/bar/exam")
def exam_bar():
    max_count = len(games.exam_bar_data)
    count = 1
    if not request.args.get("exam_count"):
        data = games.exam_bar_data[count - 1]
        serving = data["wrong_serving"].copy()
        serving.append(data["serving"])
        shuffle(serving)
        data["serving_short"] = short_value(data["serving"])
        return render_template("exam_bar.html", section=data["section"], name=data["name"], serving=serving,
                               true_ans=data, count=count, max_count=max_count)
    else:
        count = int(request.args.get("exam_count"))
        # if request.args.get("user_id"):
        #     user_id = int(request.args.get("user_id"))
        #     mistake = bool(request.args.get("mistake"))
        #     if mistake:
        #         db.add_user_mistakes(user_id, ("drinks_mistakes", games.exam_bar_data[count - 1]["id"]))

        count += 1

        data = games.exam_bar_data[count - 1]
        serving = data["wrong_serving"].copy()
        serving.append(data["serving"])
        shuffle(serving)

        serving = {short_value(key): key for key in serving}

        data["serving_short"] = short_value(data["serving"])
        resp = {
            "count": count,
            "section": data["section"],
            "name": data["name"],
            "serving": serving,
            "true_ans": data
        }
        if count == max_count:
            return make_response(resp, 201)
        else:
            return make_response(resp, 200)


@app.get("/cocktails/exam")
def exam_cocktails():
    max_count = len(games.exam_cocktails_data)
    count = 1
    if not request.args.get("exam_count"):
        data = games.exam_cocktails_data[count - 1]
        ingredients = data["wrong_ingredients"].copy()
        ingredients += data["ingredients"]
        shuffle(ingredients)
        return render_template("exam_cocktails.html", section=data["section"], name=data["name"],
                               img_path=data["img_path"], true_ans=data, count=count, max_count=max_count,
                               ingredients=ingredients)
    else:
        count = int(request.args.get("exam_count"))
        # if request.args.get("user_id"):
        #     user_id = int(request.args.get("user_id"))
        #     mistake = bool(request.args.get("mistake"))
        #     if mistake:
        #         db.add_user_mistakes(user_id, ("cocktails_mistakes", games.exam_cocktails_data[count - 1]["id"]))

        count += 1

        data = games.exam_cocktails_data[count - 1]
        ingredients = data["wrong_ingredients"].copy()
        ingredients += data["ingredients"]
        shuffle(ingredients)
        resp = {
            "count": count,
            "section": data["section"],
            "name": data["name"],
            "ingredients": ingredients,
            "true_ans": data
        }
        if count == max_count:
            return make_response(resp, 201)
        else:
            return make_response(resp, 200)


@app.get("/menu/exam")
def exam_menu():
    max_count = len(games.exam_menu_data)
    count = 1
    if not request.args.get("exam_count"):
        data = games.exam_menu_data[count - 1]
        serving = data["wrong_serving"].copy()
        serving.append(data["serving"])
        shuffle(serving)
        data["serving_short"] = short_value(data["serving"])
        return render_template("exam_menu.html", section=data["section"], name=data["name"], serving=serving,
                               true_ans=data, count=count, max_count=max_count, description=data["description"])
    else:
        count = int(request.args.get("exam_count"))
        # if request.args.get("user_id"):
        #     user_id = int(request.args.get("user_id"))
        #     mistake = bool(request.args.get("mistake"))
        #     if mistake:
        #         db.add_user_mistakes(user_id, ("meal_mistakes", games.exam_menu_data[count - 1]["id"]))

        count += 1

        data = games.exam_menu_data[count - 1]
        serving = data["wrong_serving"].copy()
        serving.append(data["serving"])
        shuffle(serving)

        serving = {short_value(key): key for key in serving}

        data["serving_short"] = short_value(data["serving"])
        resp = {
            "count": count,
            "section": data["section"],
            "name": data["name"],
            "serving": serving,
            "true_ans": data,
            "description": data["description"]
        }
        if count == max_count:
            return make_response(resp, 201)
        else:
            return make_response(resp, 200)


# @app.get("/bar/mistakes")
# def mistakes_bar():
#     max_count = int(request.args.get("mistakes_count"))
#     user_id = int(request.args.get("user_id"))
#     user = db.read_user(user_id)
#     if request.args.get("mistake_id"):
#         mistake_id = int(request.args.get("mistake_id"))
#         db.delete_user_mistakes(user_id, ("drinks_mistakes", mistake_id))
#
#     state, data = games.mistakes("bar", user.drinks_mistakes)
#     serving = data["wrong_serving"].copy()
#     serving.append(data["serving"])
#     shuffle(serving)
#     data["serving_short"] = short_value(data["serving"])
#     return render_template("exam_bar.html", title="bar mistakes", section=data["section"], name=data["name"],
#                            serving=serving, true_ans=data, count=count, max_count=max_count)



@app.post("/result")
def show_result():
    results = request.json
    return render_template("exam_result.html", results=results)


@app.get("/error")
def error():
    return render_template("error.html", status_code=request.args["status_code"])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2002)
