from sys import exc_info
from itertools import chain
from os import getenv
from dotenv import load_dotenv
import psycopg2 as pg
from Objects import Meal, Drink, Cocktail, User


def error_print(err) -> None:
    err_type, err_obj, traceback = exc_info()
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")


class DataBase:
    def __init__(self, db: str, user: str, host: str, password: str):
        try:
            self.connection = pg.connect(f"dbname={db} user={user} host={host} password={password}")
        except pg.OperationalError as e:
            error_print(e)
            self.connection = None
        else:
            print("Successful connected.")
            self.cursor = self.connection.cursor()
            self.all_meals_id = self.read_all_meals_id()
            self.all_drinks_id = self.read_all_drinks_id()
            self.all_cocktails_id = self.read_all_cocktails_id()
            # self.all_prices = self.read_all_prices()

    def create_meal(self, meal: Meal) -> None:
        if self.connection:
            try:
                self.cursor.execute("""
                    INSERT INTO meals VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    );
                """, meal.trans_to_iterable())
                self.all_meals_id.append(meal.id)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
        else:
            print("Data Base doesn't connected")

    def create_drink(self, drink: Drink) -> None:
        if self.connection:
            try:
                self.cursor.execute("""
                    INSERT INTO drinks VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    );
                """, drink.trans_to_iterable())
                self.all_drinks_id.append(drink.id)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
        else:
            print("Data Base doesn't connected")

    def create_cocktail(self, cocktail: Cocktail) -> None:
        if self.connection:
            try:
                self.cursor.execute("""
                    INSERT INTO cocktails VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    );
                """, cocktail.trans_to_iterable())
                self.all_cocktails_id.append(cocktail.id)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
        else:
            print("Data Base doesn't connected")

    def read_meal(self, id_: int) -> Meal or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT * FROM meals WHERE meals.id = %(id)s;
                """, {"id": id_})
                meal = Meal(*self.cursor.fetchone())
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return meal
        else:
            print("Data Base doesn't connected")
            return None

    def read_drink(self, id_: int) -> Drink or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT * FROM drinks WHERE drinks.id = %(id)s;
                """, {"id": id_})
                drink = Drink(*self.cursor.fetchone())
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return drink
        else:
            print("Data Base doesn't connected")
            return None

    def read_cocktail(self, id_: int) -> Cocktail or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT * FROM cocktails WHERE cocktails.id = %(id)s;
                """, {"id": id_})
                cocktail = Cocktail(*self.cursor.fetchone())
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return cocktail
        else:
            print("Data Base doesn't connected")
            return None

    def read_all_meals_id(self) -> list[int] or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT id FROM meals;
                """)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return [i[0] for i in self.cursor.fetchall()]
        else:
            print("Data Base doesn't connected")
            return None

    def read_all_drinks_id(self) -> list[int] or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT id FROM drinks;
                """)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return [i[0] for i in self.cursor.fetchall()]
        else:
            print("Data Base doesn't connected")
            return None

    def read_all_cocktails_id(self) -> list[int] or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT id FROM cocktails;
                """)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return [i[0] for i in self.cursor.fetchall()]
        else:
            print("Data Base doesn't connected")
            return None

    def create_user(self, user: User) -> tuple:
        if self.connection:
            try:
                self.cursor.execute("""
                    INSERT INTO users VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    );
                """, user.trans_to_iterable())
                return "Success", 200
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return "Error", 500
        else:
            print("Data Base doesn't connected")
            return "Error", 503

    def read_user(self, id_: int) -> User or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT * FROM users WHERE id = %(id)s;
                """, {"id": id_})
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return User(*self.cursor.fetchone())
        else:
            print("Data Base doesn't connected")
            return None

    def check_user(self, email_: str) -> tuple:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT email FROM users WHERE email = %(email)s;
                """, {"email": email_})
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return "Error", 500
            else:
                if self.cursor.fetchone():
                    return "Error", 409
                else:
                    return "Success", 200
        else:
            print("Data Base doesn't connected")
            return "Error", 503

    def update_user(self, id_: int, data: tuple) -> tuple:
        if self.connection:
            try:
                self.cursor.execute(f"""
                    UPDATE users SET {data[0]} = array_append({data[0]}, %(data)s)
                    WHERE id = %(id)s;
                """, {"id": id_, "data": data[1]})
                return "Success", 200
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return "Error", 500
        else:
            print("Data Base doesn't connected")
            return "Error", 503

    def sign_in(self, name_: str, password_: str) -> tuple:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT id, drinks_mistakes, meal_mistakes, cocktails_mistakes FROM users WHERE name = %(name)s 
                    AND password = %(password)s;
                """, {"name": name_, "password": password_})
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return "Error", 500
            else:
                data = self.cursor.fetchone()
                if data:
                    return {"id": data[0], "drinks_mistakes": data[1], "meal_mistakes": data[2],
                            "cocktails_mistakes": data[3]}, 200
                else:
                    return "Error", 401

        else:
            print("Data Base doesn't connected")
            return "Error", 503

    def read_all_prices(self, table_) -> list or None:
        if self.connection:
            try:
                self.cursor.execute(f"""
                    SELECT DISTINCT ON (price) price FROM {table_};
                """)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return [i[0] for i in self.cursor.fetchall()]
        else:
            print("Data Base doesn't connected")
            return None

    def read_all_volumes(self, table_) -> list or None:
        if self.connection:
            try:
                self.cursor.execute(f"""
                    SELECT DISTINCT ON (volume) volume FROM {table_};
                """)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return [i[0] for i in self.cursor.fetchall()]
        else:
            print("Data Base doesn't connected")
            return None

    def read_all_serving(self, table_) -> list or None:
        if self.connection:
            try:
                self.cursor.execute(f"""
                    SELECT DISTINCT ON (serving) serving FROM {table_};
                """)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return [i[0] for i in self.cursor.fetchall()]
        else:
            print("Data Base doesn't connected")
            return None

    def read_all_ingredients(self, table_) -> list or None:
        if self.connection:
            try:
                self.cursor.execute(f"""
                    SELECT DISTINCT ON (ingredients) ingredients FROM {table_};
                """)
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
                return None
            else:
                return list(set(chain.from_iterable([i[0] for i in self.cursor.fetchall()])))
        else:
            print("Data Base doesn't connected")
            return None

    def commit(self) -> None:
        if self.connection:
            self.connection.commit()
        else:
            print("Data Base doesn't connected")

    def close_connection(self) -> None:
        if self.connection:
            self.commit()
            self.cursor.close()
            self.connection.close()
        else:
            print("Data Base doesn't connected")

    def refresh_conn(self, db: str, user: str, host: str, password: str):
        try:
            self.connection = pg.connect(f"dbname={db} user={user} host={host} password={password}")
        except pg.OperationalError as e:
            error_print(e)
            self.connection = None
        else:
            print("Successful connected.")
            self.cursor = self.connection.cursor()


load_dotenv()
USER = getenv("USER")
HOST = getenv("HOST")
DB_PASSWORD = getenv("DB_PASSWORD")

db = DataBase("WaiterLearningProgram_db", USER, HOST, DB_PASSWORD)
