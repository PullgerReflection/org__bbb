import os
import json


def country_data():
    path_cwd = os.path.dirname(__file__)
    f = open(path_cwd + "/country.json")
    return json.load(f)
