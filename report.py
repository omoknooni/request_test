# import 2 dictonary and return 2 json file
import typing
import json
import os

T = typing.TypeVar("T")


def make_directory(target_path: str) -> None:
    os.makedirs(target_path, exist_ok=True)


def make_report(set: dict[T], filename: str) -> None:
    filename = filename if filename.endswith(".json") else filename + ".json"
    target_path = "./report"
    make_directory(target_path)
    with open(target_path + "/" + filename, "w", encoding="utf-8") as report_json:
        json.dump(set, report_json, ensure_ascii=False, indent=4)
