



my_dict = {'record1': 1, 'record2': 1, 'record3': 1, 'record4': 0}

keys_with_value_0 = []

for key, value in my_dict.items():
    if value == 0:
        keys_with_value_0.append(key)

print(keys_with_value_0)
