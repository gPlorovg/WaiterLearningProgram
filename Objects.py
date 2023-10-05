from sys import maxsize
from dataclasses import dataclass, fields


@dataclass
class Recipe:
    name: str = None
    section: str = None
    price: int = 0
    serving: str = None
    id: int = 0

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
    image_path: str = None
    volume: str = None
