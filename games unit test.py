from games import guess_price, guess_serving, guess_ingredients, exam, mistakes, match_quiz

# print(guess_price("bar"))
# print(guess_serving("menu"))
state, data = guess_ingredients()
ings = list(data["wrong_ingredients"] + data["ingredients"])
print(ings)
# print(exam("bar"))
# print(mistakes("bar", [8869155791494748776, 8349577753338735666, 6632626990900568427]))
# print(match_quiz("menu", "serving", 5))