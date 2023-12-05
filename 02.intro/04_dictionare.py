my_dict = {
    "key_1": 1,
    "key_2": 2,
    "key_3": 3,
}

# print(my_dict)
# print(my_dict["key_1"])
my_dict["key_4"] = 4
my_dict.update({"key_5":5, "key_6":6})
print(my_dict.get('key_4', "Doesnt exist:)"))
print(my_dict.items())