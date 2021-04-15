# default module
import requests as req
from bs4 import BeautifulSoup
import json

# custom module
import initial

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
                # print("status (", r.status_code, ")", now)
                check_set[now] = depth
                soup = BeautifulSoup(r.text, "html.parser")
                a_links = soup.find_all("a")
                for anchor in a_links:
                    href = anchor.attrs["href"]
                    if href == "#" or href == "/" or href.startswith("?"):
                        continue
                    elif href.startswith("https://"):
                        true_anchor = href
                    elif href != "/":
                        true_anchor = (
                            now + href[1:] if href.startswith("/") else now + href
                        )
                    dfs(true_anchor, check_set, depth + 1)
                tr_links = soup.find_all("tr")
                for anchor in tr_links:
                    if anchor.attrs.get("onclick"):
                        href = anchor.attrs["onclick"][15:]
                        true_anchor = now + href
                        dfs(true_anchor, check_set, depth + 1)
                td_links = soup.find_all("td")
                for anchor in td_links:
                    temp = anchor.find_all("a")
                    for item in temp:
                        href = (
                            item.attrs["href"]
                            if item.attrs["href"] != "/"
                            else item.attrs["href"][1:]
                        )
                        true_anchor = now + href
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
                    a_links = soup.find_all("a")
                    for anchor in a_links:
                        href = anchor.attrs["href"]
                        if href == "#" or href == "/" or href.startswith("?"):
                            continue
                        if href.startswith("http://") or href.startswith("https://"):
                            true_anchor = href
                        elif href != "/":
                            true_anchor = (
                                target_url + href[1:]
                                if href.startswith("/")
                                else target_url + href
                            )
                        check_set[true_anchor] = 0
                    tr_links = soup.find_all("tr")
                    for anchor in tr_links:
                        if anchor.attrs.get("onclick"):
                            href = anchor.attrs["onclick"][15:]
                            true_anchor = target_url + href
                            check_set[true_anchor] = 0
                    td_links = soup.find_all("td")
                    for anchor in td_links:
                        temp = anchor.find_all("a")
                        for item in temp:
                            href = (
                                item.attrs["href"]
                                if item.attrs["href"] != "/"
                                else item.attrs["href"][1:]
                            )
                            true_anchor = target_url + href
                            check_set[true_anchor] = 0
                    li_links = soup.find_all("li")
            except Exception as e:
                continue


print("<< Initial Scan >>")
inspect(
    url="192.168.0.78",
    alive_ports=[80, 400],
    word_list=word_list,
)
print("<< Done. Searched ", len(check_set), " Item(s) >>")
# dfs("http://192.168.0.78", check_set, 0)

json1 = json.dumps(check_set, indent=4)

initial_set = dict(check_set)
print("<< Searching Directory (Brute) >>")
for key in initial_set:
    dfs(key, check_set, 0)

print("<< Done. Searched ", len(check_set), " Item(s) >>")
for key in check_set:
    print("Has Link : ", key)
