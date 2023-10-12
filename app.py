from flask import Flask, render_template, make_response, request
from random import shuffle
from db_manage import db
from Objects import User
import games

app = Flask(__name__)


# STATUS CODES: 200 - user not in db, 409- user already exists, 500- req_db error, 503 - db doesn't connected
# 401 - user doesn't exist
@app.route("/")
def index():  # put application's code here
    return render_template("index.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("sign_up.html")
    elif request.method == "POST":
        req = request.json
        check_resp = db.check_user(req["email"])
        if check_resp[1] == 200:
            resp = db.create_user(User(email=req["email"], name=req["name"], password=req["password"]))
            if resp[1] == 200:
                db.commit()
        else:
            resp = check_resp
        return make_response(resp)


@app.post("/sign_in")
def sign_in():
    req = request.json
    resp = db.sign_in(name_=req["name"], password_=req["password"])
    return make_response(resp)


@app.get("/main")
def main():
    return render_template("main.html")


@app.get("/bar")
@app.get("/cocktails")
@app.get("/menu")
def task_list():
    names = list()
    if request.path == "/bar":
        names = ["guess_serving", "match_price", "match_volume", "match_serving"]
    elif request.path == "/cocktails":
        names = ["guess_ingredients", "match_price"]
    elif request.path == "/menu":
        names = ["guess_serving", "match_price", "match_serving", "match_description"]
    title = request.path.lstrip("/")
    title = title[0].upper() + title[1:]

    return render_template("quizzies_list.html", title=title, names=names)


@app.get("/bar/guess_price")
@app.get("/cocktails/guess_price")
@app.get("/menu/guess_price")
def guess_price():
    section = request.path.split("/")[1]
    state, data = games.guess_price(section)
    prices = data["wrong_prices"]
    prices.append(data["price"])
    shuffle(prices)
    if state == "Success":
        return render_template("guess_price.html", title="guess_price", section=data["section"], name=data["name"],
                               prices=prices, true_ans=data["price"])
    else:
        return make_response(500, state)


@app.template_filter("short_value")
def short_value(s: str) -> str:
    return s[:10] + str(len(s))


@app.get("/bar/guess_serving")
@app.get("/menu/guess_serving")
def guess_serving():
    section = request.path.split("/")[1]
    state, data = games.guess_serving(section)
    serving = data["wrong_serving"]
    serving.append(data["serving"])
    shuffle(serving)
    if state == "Success":
        return render_template("guess serving.html", title="guess_serving", section=data["section"], name=data["name"],
                               serving=serving, true_ans=short_value(data["serving"]))
    else:
        return make_response(500, state)


@app.get("/error")
def error():
    return render_template("error.html", status_code=request.args["status_code"])


if __name__ == '__main__':
    app.run()
