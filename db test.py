from os import getenv
from dotenv import load_dotenv
from db_manage import DataBase
from scan_data import meals_list, drink_list, cocktail_list
from Objects import Meal, Drink, Cocktail, User


load_dotenv()
USER = getenv("USER")
HOST = getenv("HOST")
DB_PASSWORD = getenv("DB_PASSWORD")

db = DataBase("WaiterLearningProgram_db", USER, HOST, DB_PASSWORD)

user = User("email", "name", "password", [1, 2], [3], [4, 5])
print(db.sign_in(user.name, user.password))

