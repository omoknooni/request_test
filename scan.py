# Default module
import typing
import requests as req
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


# Custom Module
import scrapping as scr

# temporary Module -> only for testing
import time

T = typing.TypeVar("T")


def url_setter(anchors: list[str], url_set: dict[T]) -> None:
    for anchor in anchors:
        url_set[anchor] = 0


def get_headers():
    ca = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ca.random}
    return headers


def dfs_scan(
    now: str,
    check_set: dict[T],
    depth: int,
    max_depth: int,
) -> None:
    if depth >= max_depth or (check_set.get(now) != None):
        return
    else:
        try:
            random_agent = get_headers()
            r = req.get(now, timeout=0.5, headers=random_agent)
            if r.status_code == 200:
                # print(f"[{depth}] : {now}")
                check_set[now] = depth

                soup = BeautifulSoup(r.text, "html.parser")

                true_anchors = scr.a_scrapping(soup.find_all("a"), now)
                # print("a_scrapping")
                time.sleep(0.05)
                for true_anchor in true_anchors:
                    dfs_scan(true_anchor, check_set, depth + 1, max_depth)

                # print("tr_scrapping")
                time.sleep(0.05)
                true_anchors = scr.tr_scrapping(soup.find_all("tr"), now)
                for true_anchor in true_anchors:
                    dfs_scan(true_anchor, check_set, depth + 1, max_depth)

                # print("td_scrapping")
                time.sleep(0.05)
                true_anchors = scr.td_scrapping(soup.find_all("td"), now)
                for true_anchor in true_anchors:
                    dfs_scan(true_anchor, check_set, depth + 1, max_depth)

                # print("li_scrapping")
                time.sleep(0.05)
                true_anchors = scr.li_scrapping(soup.find_all("li"), now)
                for true_anchor in true_anchors:
                    dfs_scan(true_anchor, check_set, depth + 1, max_depth)

            else:
                return
        except Exception:
            return


def initial_scan(
    url: str,
    alive_ports: list[int],
    word_list: list[str],
    url_set: dict[T],
    timeout: float,
) -> None:
    if not url.startswith("http://"):
        url = "http://" + url
    for port in alive_ports:
        start_url = url + ":" + f"{port}/"
        for word in word_list:
            try:
                target_url = start_url + word
                random_agent = get_headers()
                r = req.get(target_url, timeout=0.5, headers=random_agent)
                if r.status_code == 200:
                    url_set[target_url] = 0
                    soup = BeautifulSoup(r.text, "html.parser")

                    true_anchors = scr.a_scrapping(soup.find_all("a"), target_url)
                    url_setter(true_anchors, url_set)

                    true_anchors = scr.tr_scrapping(soup.find_all("tr"), target_url)
                    url_setter(true_anchors, url_set)

                    true_anchors = scr.td_scrapping(soup.find_all("td"), target_url)
                    url_setter(true_anchors, url_set)

                    true_anchors = scr.li_scrapping(soup.find_all("li"), target_url)
                    url_setter(true_anchors, url_set)
            except Exception:
                continue


def scan_entry(conf: list):
    # get data from conf
    url, word_list, max_depth, timeout, url_set, port = conf
    alive_ports = [
        port,
    ]
    # initial_scan
    print("<< [3-1] : Initial Scan >>")
    initial_scan(url, alive_ports, word_list, url_set, timeout)
    initial_set = dict(url_set)
    print("<< [3-1] : Done. Searched ", len(url_set), " Item(s) >>")
    print("<< [3-2] : Searching Directory (Brute) >>")
    for URL in initial_set:
        dfs_scan(URL, url_set, 0, max_depth)
    print(
        "<< [3-2] : Done. Searched ", len(url_set) - len(initial_set), "new Item(s) >>"
    )
    """
    for URL in url_set:
        print("Has Link : ", URL)
    """

    return initial_set, url_set