import demjson


def estimator(data):
    data = demjson.decode(data)
    print(data)
    return data
