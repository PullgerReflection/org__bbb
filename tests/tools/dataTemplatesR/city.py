import os
import json


def city_data():
    path_cwd = os.path.dirname(__file__)
    f = open(path_cwd + "/city.json")
    return json.load(f)
