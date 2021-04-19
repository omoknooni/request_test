# import 2 dictonary and return 2 json file
import typing
import json
import os

T = typing.TypeVar("T")


def make_directory(target_path: str) -> None:
    os.makedirs(target_path, exist_ok=True)


def make_report(set: dict[T], workfolder, filename: str) -> None:
    filename = filename if filename.endswith(".json") else filename + ".json"
    make_directory(workfolder)
    with open(os.path.join(workfolder, filename), "w", encoding="utf-8") as report_json:
        json.dump(set, report_json, ensure_ascii=False, indent=4)
    print("Report Saved : ", os.path.join(workfolder, filename))
