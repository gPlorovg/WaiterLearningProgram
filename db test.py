from os import getenv
from dotenv import load_dotenv
from db_manage import DataBase
from scan_data import meals_list, drink_list, cocktail_list
from Objects import Meal, Drink, Cocktail


load_dotenv()
USER = getenv("USER")
HOST = getenv("HOST")
DB_PASSWORD = getenv("DB_PASSWORD")

db = DataBase("WaiterLearningProgram_db", USER, HOST, DB_PASSWORD)
for obj in cocktail_list:
    print(obj)
    db.create_cocktail(obj)

for obj in cocktail_list:
    print(obj)
    print(db.read_cocktail(obj.id))
