def create_ref(data, key_index, value_index):
    ref = {}
    for row in data:
        ref[row[key_index]] = row[value_index]
    return ref
