from sys import maxsize
from dataclasses import dataclass, fields


# Objects must have same order of fields like order in db table!
@dataclass
class Recipe:
    id: int = 0
    name: str = None
    section: str = None
    price: int = 0
    serving: str = None

    def trans_to_iterable(self) -> list:
        resp = list()
        for f in fields(self):
            resp.append(getattr(self, f.name))
        return resp

    def __post_init__(self):
        self.id = hash(self.name + self.section) % (maxsize + 1)


@dataclass
class Meal(Recipe):
    description: str = None


@dataclass
class Drink(Recipe):
    volume: str = None


@dataclass
class Cocktail(Recipe):
    ingredients: list[str] = None
    volume: str = None
    image_path: str = None
