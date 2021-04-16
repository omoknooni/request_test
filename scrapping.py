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
        print(href)
        true_anchors.append(true_anchor)
    return true_anchors


def tr_scrapping(tr_links, target_url):
    true_anchors = list()
    for anchor in tr_links:
        if anchor.attrs.get("onclick"):
            href = anchor.attrs["onclick"][15:]
            href = href if not href.startswith("./") else href[2:]

            print(href)
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
                if item.attrs["href"] != "/" and item.attrs["href"] != "#"
                else item.attrs["href"][1:]
            )
            print(href)
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
            if href == "#":
                continue
            print(href)
            true_anchor = target_url + href
            true_anchors.append(true_anchor)

    return true_anchors
