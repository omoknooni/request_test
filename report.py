# import 2 dictonary and return 2 json file
import json


def initial_report(initial_set):
    with open("./reports/initial.json", "w", encoding="utf-8") as initial_json:
        json.dump(initial_set, initial_json, ensure_ascii=False, indent=4)


def final_report(final_set):
    with open("./reports/final.json", "w", encoding="utf-8") as final_json:
        json.dump(final_set, final_json, ensure_ascii=False, indent=4)