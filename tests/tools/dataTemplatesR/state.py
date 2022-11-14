import os
import json


def state_data():
    path_cwd = os.path.dirname(__file__)
    f = open(path_cwd + "/state.json")
    return json.load(f)
