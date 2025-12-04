import helper_functions

helper_functions.store_data("high_scores.json", 1)
helper_functions.store_data("high_scores.json", 1)
print("data stored")
print(helper_functions.load_data("high_scores.json"))
print("data loaded")
