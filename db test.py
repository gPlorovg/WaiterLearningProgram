from db_manage import db
from scan_data import meals_list, drink_list, cocktail_list
from Objects import Meal, Drink, Cocktail, User


user = User(0, "emai_3", "name", "password", [1, 2], [3], [4, 5])
print(db.create_user(user))
print(db.sign_in(user.name, user.password))
print(db.read_user(user.id))
print(db.check_user(user.email))
print(db.update_user(user.id, ("drinks_mistakes", [6, 7])))
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
