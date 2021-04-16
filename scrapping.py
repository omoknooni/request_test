# default module

from bs4 import BeautifulSoup


def a_scrapping(a_links, target_url):
    true_anchors = list()
    for anchor in a_links:
        href = anchor.attrs["href"]
        if href == "#" or href == "/" or href.startswith("?"):
            continue
        if href.startswith("http://") or href.startswith("https://"):
            true_anchor = href
        elif href != "/":
            true_anchor = (
                target_url + href[1:] if href.startswith("/") else target_url + href
            )
        true_anchors.append(true_anchor)
    return true_anchors


def tr_scrapping(tr_links, target_url):
    true_anchors = list()
    for anchor in tr_links:
        if anchor.attrs.get("onclick"):
            href = anchor.attrs["onclick"][15:]
            true_anchor = target_url + href
            true_anchors.append(true_anchor)
    return true_anchors


def td_scrapping(td_links, target_url):
    true_anchors = list()
    for anchor in td_links:
        temp = anchor.find_all("a")
        for item in temp:
            href = (
                item.attrs["href"]
                if item.attrs["href"] != "/"
                else item.attrs["href"][1:]
            )
            true_anchor = target_url + href
            true_anchors.append(true_anchor)
            # check_set[true_anchor] = 0
    return true_anchors


def li_scrapping(li_links, target_url):
    true_anchors = list()
    for anchor in li_links:
        temp = anchor.find_all("a")
        for item in temp:
            href = item.attrs["href"]
            if href.startswith("/"):
                href = href[1:]
            true_anchor = target_url + href
            true_anchors.append(true_anchor)

    return true_anchors


""" 
import requests as req
# custom module
import initial

url, word_list, max_depth, timeout, check_set, alive_ports = initial.settings()


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
                    print(len(soup.find_all("a")))
                    true_anchors = a_scrapping(soup.find_all("a"), target_url)
                    check(true_anchors, check_set)

                    print(len(soup.find_all("tr")))
                    true_anchors = tr_scrapping(soup.find_all("tr"), target_url)
                    check(true_anchors, check_set)

                    print(len(soup.find_all("td")))
                    true_anchors = td_scrapping(soup.find_all("td"), target_url)
                    check(true_anchors, check_set)

                    li_links = soup.find_all("li")
            except Exception as e:
                continue


inspect(url, alive_ports, word_list)

print(len(check_set))
for key in check_set.keys():
    print("key : ", key)

"""
