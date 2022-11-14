import os
import json


def category_data():
    path_cwd = os.path.dirname(__file__)
    f = open(path_cwd + "/category.json")
    return json.load(f)
