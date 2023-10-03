from dataclasses import dataclass, fields


@dataclass
class Recipe:
    name: str = None
    ingredients: list[str] = None
    price: int = 0
    serving: str = None

    def trans_to_iterable(self) -> list:
        resp = list()
        for f in fields(self):
            resp.append(getattr(self, f.name))
        return resp


@dataclass
class Meal(Recipe):
    course: str = None
    alternatives: list[str] = None
    meal_matches: list[str] = None
    drink_matches: list[str] = None


@dataclass
class Drink(Recipe):
    value: int = 0
    alternatives: list[str] = None
    meal_matches: list[str] = None
