# Default module
import requests as req
from bs4 import BeautifulSoup


# Custom Module
import initial
from scrapping import *
from report import initial_report, final_report

url, word_list, max_depth, timeout, url_set, alive_ports = initial.settings()
dead_port = list()
# Searching for Ports


def url_setter(anchors, url_set):
    for anchor in anchors:
        url_set[anchor] = 0


def port_scan(url, alive_ports, dead_ports):
    for port in range(10, 8080, 10):
        target_url = url + ":" + f"{port}"
        print(target_url)
        if len(alive_ports) >= 2:
            break
        try:
            print("ALIVE : ", port)
            alive_ports.append(port)
        except Exception:
            dead_ports.append(port)


def dfs_scan(now, check_set, depth):
    if depth >= max_depth or (
        check_set.get(now) != None and int(check_set.get(now) >= max_depth)
    ):
        return
    else:
        try:
            r = req.get(now, timeout=1)
            if r.status_code == 200:
                check_set[now] = depth

                soup = BeautifulSoup(r.text, "html.parser")

                true_anchors = a_scrapping(soup.find_all("a"), now)
                for true_anchor in true_anchors:
                    dfs_scan(true_anchor, check_set, depth + 1)

                true_anchors = tr_scrapping(soup.find_all("tr"), now)
                for true_anchor in true_anchors:
                    dfs_scan(true_anchor, check_set, depth + 1)

                true_anchors = td_scrapping(soup.find_all("td"), now)
                for true_anchor in true_anchors:
                    dfs_scan(true_anchor, check_set, depth + 1)
                true_anchors = li_scrapping(soup.find_all("li"), now)
                for true_anchor in true_anchors:
                    dfs_scan(true_anchor, check_set, depth + 1)

            else:
                return
        except Exception:
            return


def initial_scan(url, alive_ports, word_list):
    initial_set = dict()

    if not url.startswith("http://"):
        url = "http://" + url
    for port in alive_ports:
        start_url = url + ":" + f"{port}/"
        for word in word_list:
            try:
                target_url = start_url + word
                r = req.get(target_url, timeout=0.5)
                if r.status_code == 200:
                    url_set[target_url] = 0
                    soup = BeautifulSoup(r.text, "html.parser")

                    true_anchors = a_scrapping(soup.find_all("a"), target_url)
                    url_setter(true_anchors, url_set)

                    true_anchors = tr_scrapping(soup.find_all("tr"), target_url)
                    url_setter(true_anchors, url_set)

                    true_anchors = td_scrapping(soup.find_all("td"), target_url)
                    url_setter(true_anchors, url_set)

                    true_anchors = li_scrapping(soup.find_all("li"), target_url)
                    url_setter(true_anchors, url_set)
            except Exception:
                continue
    return initial_set


print("<< Initial Scan >>")
initial_set = initial_scan(url, alive_ports, word_list)
print("<< Done. Searched ", len(url_set), " Item(s) >>")

for URL in initial_set:
    print("URL : ", URL)


print("<< Searching Directory (Brute) >>")
for URL in initial_set:
    dfs_scan(URL, url_set, 0)

print("<< Done. Searched ", len(url_set), " Item(s) >>")
for URL in url_set:
    print("Has Link : ", URL)

initial_report(initial_set)
final_report(url_set)