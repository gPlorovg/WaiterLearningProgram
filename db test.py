from db_manage import db
from scan_data import meals_list, drink_list, cocktail_list
from Objects import Meal, Drink, Cocktail, User


user = User(0, "emai", "name", "password", [1, 2], [3])
print(db.create_user(user))
print(db.sign_in(user.name, user.password))
print(db.read_user(user.id))
print(db.add_user_mistakes(user.id, ("cocktails_mistakes", 5)))
print(db.delete_user_mistakes(user.id, ("meal_mistakes", 3)))
print(db.read_user(user.id))

# for obj in meals_list:
#     db.create_meal(obj)
#
# for obj in drink_list:
#     db.create_drink(obj)
#
# for obj in cocktail_list:
#     db.create_cocktail(obj)
#
# db.commit()
