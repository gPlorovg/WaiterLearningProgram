import Objects


meal = Objects.Meal(name="Цезарь", ingredients=["Курица", "Салат", "Соус цезарь", "Помидор"], price=300,
                    serving="Тарелка", course="Первый", alternatives=["Греческий салат", "Фунчоза"],
                    meal_matches=["Ризотто", "Луковый суп"], drink_matches=["Белое вино", "Московский мул"])
drink = Objects.Drink(name="Лонг Айленд", ingredients=["Водка", "Сок лайма", "Имбирное пиво"], price=500,
                    serving="Медная кружка", value=200, alternatives=["Лонг Айленд", "Зелёная фея"],
                    meal_matches=["Фруктовая тарелка"])
print(meal)
print(drink)
print(meal.trans_to_iterable())
print(drink.trans_to_iterable())
