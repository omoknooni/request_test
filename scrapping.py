# default module
import typing

from typing import Callable, AnyStr
from bs4 import BeautifulSoup


def decorator(func: Callable) -> Callable:
    def decorator(*args):
        # print(func.__name__)
        result = func(*args)
        return result

    return decorator


@decorator
def a_scrapping(a_links: list[str], target_url: str) -> list[str]:
    true_anchors = list()
    for anchor in a_links:
        href = anchor.attrs["href"]
        if href.startswith("#") or href == "/" or href.startswith("?"):
            continue
        if href.startswith("http://") or href.startswith("https://"):
            true_anchor = href
        elif href != "/":
            true_anchor = (
                target_url + href[1:] if href.startswith("/") else target_url + href
            )
        true_anchors.append(true_anchor)
    return true_anchors


@decorator
def tr_scrapping(tr_links: list[str], target_url: list) -> list[str]:
    true_anchors = list()
    for anchor in tr_links:
        if anchor.attrs.get("onclick"):
            href = anchor.attrs["onclick"][15:]
            href = href if not href.startswith("./") else href[2:]
            true_anchor = target_url + href
            true_anchors.append(true_anchor)
    return true_anchors


@decorator
def td_scrapping(td_links: list[str], target_url: str) -> list[str]:
    true_anchors = list()
    for anchor in td_links:
        temp = anchor.find_all("a")
        for item in temp:
            href = (
                item.attrs["href"]
                if item.attrs["href"] != "/" and item.attrs["href"] != "#"
                else item.attrs["href"][1:]
            )
            true_anchor = target_url + href
            true_anchors.append(true_anchor)
    return true_anchors


@decorator
def li_scrapping(li_links: list[str], target_url: str) -> list[str]:
    true_anchors = list()
    for anchor in li_links:
        temp = anchor.find_all("a")
        for item in temp:
            href = item.attrs["href"]
            if href.startswith("/"):
                href = href[1:]
            if href == "#" or href.startswith("https://") or href.startswith("http://"):
                continue
            true_anchor = target_url + href
            true_anchors.append(true_anchor)

    return true_anchors
