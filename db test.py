from os import getenv
from dotenv import load_dotenv
from random import sample, randint, choice
from db_manage import DataBase
import Objects


meal = Objects.Meal(name="Цезарь", ingredients=["Курица", "Салат", "Соус цезарь", "Помидор"], price=300,
                    serving="Тарелка", course="Первый", alternatives=["Греческий салат", "Фунчоза"],
                    meal_matches=["Ризотто", "Луковый суп"], drink_matches=["Белое вино", "Московский мул"])
drink = Objects.Drink(name="Лонг Айленд", ingredients=["Водка", "Сок лайма", "Имбирное пиво"], price=500,
                    serving="Медная кружка", value=200, alternatives=["Лонг Айленд", "Зелёная фея"],
                    meal_matches=["Фруктовая тарелка"])
meal2 = Objects.Meal(name="Оливье", ingredients=["Курица", "Салат", "Соус цезарь", "Помидор"], price=400,
                    serving="Тарелка", course="Первый", alternatives=["Греческий салат", "Фунчоза"],
                    meal_matches=["Ризотто", "Луковый суп"], drink_matches=["Белое вино", "Московский мул"])
drink2 = Objects.Drink(name="Водка Редбул", ingredients=["Водка", "Сок лайма", "Имбирное пиво"], price=600,
                    serving="Медная кружка", value=200, alternatives=["Лонг Айленд", "Зелёная фея"],
                    meal_matches=["Фруктовая тарелка"])

load_dotenv()
USER = getenv("USER")
HOST = getenv("HOST")
DB_PASSWORD = getenv("DB_PASSWORD")

db = DataBase("WaiterLearningProgram_db", USER, HOST, DB_PASSWORD)
NAMES_MEAL = ["Оливье", "Цезарь", "Осенний салат с печёной тыквой и свёклой",
         "Салат из печёных баклажанов с соусом гамадари","Чизбургер", "Ролл с говяжьей колбаской и картофельным пюре",
         "Брускетта 4 сыра и конфи из инжира","Жареный сыр бри с конфи из инжира", "Согревающий томатный суп",
         "Киш с курицей и грибами"]
NAMES_DRINK = ["Московский мул", "Лонг Айленд","Негрони", "Американо", "Сухой мартини", "Манхеттен", "Гимлет", "Белая леди",
         "Кислый виски", "Джин тоник"]
names = NAMES_MEAL.copy()
ingredients = ["INGREDIENT" + str(i) for i in range(20)]
courses = ["Закуска", "Первый курс", "Второй курс", "Третий курс"]
prices = [300, 400, 410, 490, 490, 330, 350, 650, 390, 370]
for _ in range(10):
    meal = Objects.Meal(name=names.pop(), ingredients=sample(ingredients, randint(3, 6)), price=prices.pop(),
                    serving="Тарелка", course=choice(courses), alternatives=sample(NAMES_MEAL, randint(2, 4)),
                    meal_matches=sample(NAMES_MEAL, randint(2, 4)), drink_matches=sample(NAMES_DRINK, randint(1, 3)))
    db.create_meal(meal)
names = NAMES_DRINK.copy()
prices = [500, 600, 500, 500, 500, 500, 600, 600, 600, 450]
for _ in range(10):
    drink = Objects.Drink(name=names.pop(), ingredients=sample(ingredients, randint(3, 6)), price=prices.pop(),
                    serving="Медная кружка", value=350, alternatives=sample(NAMES_DRINK, randint(1, 3)),
                    meal_matches=sample(NAMES_MEAL, randint(2, 4)))
    db.create_drink(drink)
db.commit()
# db.create_meal(meal)
# db.create_meal(meal2)
#
# db.create_drink(drink)
# db.create_drink(drink2)

print(db.read_all_meals())
print(db.read_all_drinks())
