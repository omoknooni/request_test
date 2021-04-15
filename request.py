# default module
import requests as req
from bs4 import BeautifulSoup
import json

# custom module
import initial
from scrapping import *

url, word_list, max_depth, timeout, check_set, alive_ports = initial.settings()
dead_port = list()
# Searching for Ports


def port_scan(url, alive_ports, dead_ports):
    for port in range(10, 8080, 10):
        target_url = url + ":" + f"{port}"
        print(target_url)
        if len(alive_ports) >= 2:
            break
        try:
            r = req.get(target_url)
            print("ALIVE : ", port)
            alive_ports.append(port)
        except Exception:
            dead_ports.append(port)


def dfs(now, check_set, depth):
    # now = now + "/" if not now.endswith("/") else now
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
                    dfs(true_anchor, check_set, depth + 1)

                true_anchors = tr_scrapping(soup.find_all("tr"), now)
                for true_anchor in true_anchors:
                    dfs(true_anchor, check_set, depth + 1)

                true_anchors = td_scrapping(soup.find_all("td"), now)
                for true_anchor in true_anchors:
                    dfs(true_anchor, check_set, depth + 1)
                li_links = soup.find_all("li")
            else:
                return
        except Exception as e:
            return


def inspect(url, alive_ports, word_list):
    if not url.startswith("http://"):
        url = "http://" + url
    for port in alive_ports:
        start_url = url + ":" + f"{port}/"
        for word in word_list:
            try:
                target_url = start_url + word
                r = req.get(target_url, timeout=0.5)
                if r.status_code == 200:
                    check_set[target_url] = 0
                    soup = BeautifulSoup(r.text, "html.parser")
                    true_anchors = a_scrapping(soup.find_all("a"), target_url)
                    check(true_anchors, check_set)

                    true_anchors = tr_scrapping(soup.find_all("tr"), target_url)
                    check(true_anchors, check_set)

                    true_anchors = td_scrapping(soup.find_all("td"), target_url)
                    check(true_anchors, check_set)

                    li_links = soup.find_all("li")
            except Exception as e:
                continue


print("<< Initial Scan >>")
inspect(url, alive_ports, word_list)
print("<< Done. Searched ", len(check_set), " Item(s) >>")

initial_set = dict(check_set)
for key in initial_set:
    print("key : ", key)


print("<< Searching Directory (Brute) >>")
for key in initial_set:
    dfs(key, check_set, 0)

print("<< Done. Searched ", len(check_set), " Item(s) >>")
for key in check_set:
    print("Has Link : ", key)


# json1 = json.dumps(check_set, indent=4)
