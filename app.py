from flask import Flask, render_template, make_response, request
from os import getenv
from dotenv import load_dotenv
from db_manage import DataBase
from Objects import User


load_dotenv()
USER = getenv("USER")
HOST = getenv("HOST")
DB_PASSWORD = getenv("DB_PASSWORD")

db = DataBase("WaiterLearningProgram_db", USER, HOST, DB_PASSWORD)

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
        names = ["guess_serving", "match_price_and_volume", "match_serving"]
    elif request.path == "/cocktails":
        names = ["guess_ingredients", "match_price_and_volume"]
    elif request.path == "/menu":
        names = ["guess_serving", "match_price", "match_serving", "match_description"]
    title = request.path.lstrip("/")
    title = title[0].upper() + title[1:]

    return render_template("task_list.html", title=title, names=names)


@app.get("/error")
def error():
    return render_template("error.html", status_code=request.args["status_code"])


if __name__ == '__main__':
    app.run()
