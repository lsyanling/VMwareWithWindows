def get_object_field_keys(obj):
    result = ""
    for key, value in vars(obj).items():
        if isinstance(value, (int, float, str)):
            result += key + ','
    return result

def get_object_field_values(obj):
    result = ""
    for key, value in vars(obj).items():
        if isinstance(value, (int, float, str)):
            result += str(value) + ','
    return result