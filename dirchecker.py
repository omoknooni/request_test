import argparse
import requests
import time
import re
import json
from colorama import init, Fore, Back
from random import uniform
from fake_useragent import UserAgent

init(autoreset=True)
df = {}

# Sanitize URL to request
def ck_url(url, port):
    if ("http" not in url) and (port == 80 or port == 8000):
        url = "http://" + url
        print(f"[!] URL changed : {url}")
    elif ("http" not in url) and port == 443:
        url = "https://" + url
        print(f"[!] URL changed! : {url}")
    elif port != 80 or port != 8000 or port != 443:
        url = "http://" + url + ":" + port
        print(f"[!] URL changed!! : {url}")
    return url


def dir_crawl(url, d_lists, argz):
    find = []
    randomAgent = argz.random_agent
    delay = argz.delay
    dirpath = argz.dir_path

    headers = {"User-Agent": "python-dirchecker"}
    if randomAgent == True:
        print("[!] Random-Agent mode ON")
        ua = UserAgent()

    # Read dir_name file and make request URL
    for dirc in d_lists:
        # dirc = dirc.replace("\n", "")
        dirc = "/" + dirc
        search_url = url + dirc
        print(f"[?] Checking {search_url} ...", end="")

        if randomAgent == True:
            headers = {"User-Agent": ua.random}

        try:
            res = requests.get(search_url, headers=headers)
            res_code = res.status_code
        except requests.exceptions.Timeout as tmo:
            print(Fore.BLACK + Back.RED + "[!] Timeout : ", tmo)
            exit()
        except requests.exceptions.ConnectionError as ce:
            print(Fore.BLACK + Back.RED + "[!] Connection Error : ", ce)
            exit()

        # Put delay
        time.sleep(round(uniform(delay * 0.5, delay * 1.5)))

        if res_code != 404:
            print(Fore.BLUE + Back.GREEN + "[O] Found!")
            find.append(dirc)
        else:
            print(Fore.BLACK + Back.YELLOW + "[X] 404 NOT FOUND")
    return find


def file_crawl(df, f_lists, ext_lists, url, d_found, dir_res, argz):
    find = []
    randomAgent = argz.random_agent
    delay = argz.delay

    headers = {"User-Agent": "python-dirchecker"}
    if randomAgent == True:
        print("[+] Random Agent mode on")
        ua = UserAgent()

    for d in d_found:
        find = []
        for dirc in dir_res:
            if d not in dirc:
                continue
            for f in f_lists:
                f = f.replace("\n", "")
                for ext in ext_lists:
                    search_url = url + dirc + "/" + f + ext
                    print(f"[?] Checking {search_url} ...", end="")

                    if randomAgent == True:
                        headers = {"User-Agent": ua.random}

                    try:
                        res = requests.get(search_url, headers=headers)
                        res_code = res.status_code
                    except requests.exceptions.Timeout as tmo:
                        print(Fore.BLACK + Back.RED + "[!] Timeout : ", tmo)
                        exit()
                    except requests.exceptions.ConnectionError as ce:
                        print(Fore.BLACK + Back.RED + "[!] Connection Error : ", ce)
                        exit()

                    # Put delay
                    time.sleep(round(uniform(delay * 0.5, delay * 1.5)))

                    if res_code != 404:
                        print(Fore.BLUE + Back.GREEN + "[O] Found!")
                        find.append(search_url)
                    else:
                        print(Fore.BLACK + Back.YELLOW + "[X] 404 NOT FOUND")
        if find:
            df[d].append(find)
    return find


def deep_dir_scan(url, d_found, d_lists, arg):
    dir_dict = {}
    for d in d_found:
        save = [""]
        tmp = []
        dir_dict[d] = []
        while len(save) != 0:
            search_url = url + d + save[0]
            tmp = dir_crawl(search_url, d_lists, arg)
            if dir_dict[d]:
                tmp = list(
                    map(lambda x: save[0] + x, tmp)
                )  # 앞에 save[0] 경로 추가 ['/admin'] -> ['/css/admin']

            save.extend(tmp)
            save.pop(0)
            dir_dict[d].extend(tmp)

    print(f"[*] Indexable Directory Result : {dir_dict}")
    return dir_dict


def dirchecker_entry(arg, dir_list: list, name_list: list, ext_list: list):
    print(arg)
    d_found, f_found, exts = [], [], []
    dir_book, name_book, ext_book = [], [], []

    start = time.time()

    port = arg.port
    arg.url = ck_url(arg.url, port)
    url = arg.url
    dirpath = arg.dir_path
    fnmpath = arg.fnm_path
    extpath = arg.ext_path

    # Read txt files
    dir_book = dir_list
    name_book = name_list
    ext_book = ext_list

    # Finding primary directory name
    d_found = dir_crawl(url, dir_book, arg)
    print(f"[*] Discovered Indexable Directory : {d_found}")

    # Finding deep directory name -> 모듈화 필요?
    # input : d_found(1차적으로 검색한 dirname), dir_book(디렉토리 이름 파일을 읽은 리스트)
    # output : df(json으로 저장시킬 dic)
    if d_found:
        df = deep_dir_scan(url, d_found, dir_book, arg)

    # file discovery
    dir_res = []
    for i in df.keys():
        dir_res.append(i)
        for j in df[i]:
            dir_res.append(i + j)
    print(f"[*] Dir to searching File : {dir_res}")

    try:
        f_found = file_crawl(df, name_book, ext_book, url, d_found, dir_res, arg)
    except:
        print(f"[!] Finding file executed incompletely....")
        exit()
    print(f"[*] Finding file successfully complete!")

    # Save as json
    now = time.strftime("%Y%m%d%H%M%S")

    if "https://" in url:
        url = url.strip("https://")
    else:
        url = url.strip("http://")
    name = url + "_" + now + ".json"
    name = re.sub('[\/:*?"<>|]', "_", name)
    with open("./reports/" + name, "w") as jo:
        json.dump(df, jo, indent=2)
    total = round(time.time() - start, 3)
    print(f"[*] Result has exported to JSON : {name}\n>> Time elapsed : {total}s")
