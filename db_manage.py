from sys import exc_info
import psycopg2 as pg
from Objects import Meal, Drink


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
            self.all_meals = self.read_all_meals()
            self.all_drinks = self.read_all_drinks()

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
                    %s,
                    %s,
                    %s
                    );
                """, meal.trans_to_iterable())
                self.all_meals += meal.name
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
                    %s,
                    %s
                    );
                """, drink.trans_to_iterable())
                self.all_drinks += drink.name
            except pg.ProgrammingError as e:
                error_print(e)
                self.connection.rollback()
        else:
            print("Data Base doesn't connected")

    def read_meal(self, name: str) -> Meal or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT * FROM meals WHERE meals.name = %(name)s;
                """, {"name": name})
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

    def read_drink(self, name: str) -> Drink or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT * FROM drinks WHERE drinks.name = %(name)s;
                """, {"name": name})
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

    def read_all_meals(self) -> list[str] or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT name FROM meals;
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

    def read_all_drinks(self) -> list[str] or None:
        if self.connection:
            try:
                self.cursor.execute("""
                    SELECT name FROM drinks;
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
