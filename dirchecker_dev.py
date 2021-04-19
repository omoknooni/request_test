import argparse
import requests
import time
import re
import json
from colorama import init, Fore, Back
from random import uniform
from fake_useragent import UserAgent
import typing

init(autoreset=True)

# Sanitize URL to request
def ck_url(url: str, port: int) -> str:
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


def dir_crawl(url: str, d_list: list, random_agent: bool, delay: float) -> list:
    find = []

    headers = {"User-Agent": "python-dirchecker"}
    if random_agent == True:
        print("[!] Random-Agent mode ON")
        ua = UserAgent()

    # Read dir_name file and make request URL
    for dirc in d_list:
        # dirc = dirc.replace("\n", "")
        dirc = "/" + dirc
        search_url = url + dirc
        print(f"[?] Checking {search_url} ...", end="")

        if random_agent == True:
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

        if res_code != 404:
            print(Fore.BLUE + Back.GREEN + "[O] Found!")
            find.append(dirc)
        else:
            print(Fore.BLACK + Back.YELLOW + "[X] 404 NOT FOUND")

    return find


def file_crawl(
    f_lists: list,
    ext_list: list,
    url: str,
    d_found: list,
    dir_res: list,
    random_agent: bool,
    delay: float,
    df: dict,
) -> list:
    find = []

    headers = {"User-Agent": "python-dirchecker"}
    if random_agent == True:
        print("[+] Random Agent mode on")
        ua = UserAgent()

    for d in d_found:
        find = []
        for dirc in dir_res:
            if d not in dirc:
                continue

            for f in f_lists:
                f = f.replace("\n", "")
                for ext in ext_list:
                    search_url = url + dirc + "/" + f + ext
                    print(f"[?] Checking {search_url} ...", end="")

                    if random_agent == True:
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

                    if res_code != 404:
                        print(Fore.BLUE + Back.GREEN + "[O] Found!")
                        find.append(search_url)
                    else:
                        print(Fore.BLACK + Back.YELLOW + "[X] 404 NOT FOUND")
            # f_lists.close()
        if find:
            df[d].append(find)
    return find


def deep_dir_scan(
    url: str, d_found: list, d_list: list, random_agent: bool, delay: float
) -> dict:
    dir_dict = {}
    for d in d_found:
        save = [""]
        tmp = []
        dir_dict[d] = []
        while len(save) != 0:
            search_url = url + d + save[0]
            tmp = dir_crawl(search_url, d_list, random_agent, delay)
            if dir_dict[d]:
                tmp = list(
                    map(lambda x: save[0] + x, tmp)
                )  # 앞에 save[0] 경로 추가 ['/admin'] -> ['/css/admin']

            save.extend(tmp)
            save.pop(0)
            dir_dict[d].extend(tmp)

    print(f"[*] Indexable Directory Result : {dir_dict}")
    return dir_dict


def read_dir_list(dirpath: str) -> list:
    dirs = []
    try:
        d_lists = open(dirpath, "r")
    except:
        print("[!] No such file, please check the filename")
        exit()

    for directory in d_lists:
        directory = directory.replace("\n", "")
        dirs.append(directory)
    d_lists.close()
    print(f"[*] Dir : {dirs}")
    return dirs


def read_name_list(fnmpath: str) -> list:
    names = []
    try:
        f_lists = open(fnmpath, "r")
    except:
        print("[!] No such file, please check the filename")
        exit()

    for file_name in f_lists:
        file_name = file_name.replace("\n", "")
        names.append(file_name)
    f_lists.close()
    print(f"[*] Name : {names}")
    return names


def read_extension(extpath: str) -> list:
    exts = []
    try:
        ext_lists = open(extpath, "r")
    except:
        print("[!] No such file, please check the filename")
        exit()

    for extension in ext_lists:
        extension = extension.replace("\n", "")
        exts.append(extension)
    ext_lists.close()
    print(f"[*] Ext : {exts}")
    return exts


def dirchecker_entry(
    url: str,
    dir_list: list,
    fnm_list: list,
    ext_list: list,
    delay: float,
    random_agent: bool,
):
    d_found, f_found, exts = [], [], []
    df = {}
    # dir_book, name_book, ext_book = [], [], []

    start = time.time()

    # Read txt files

    # Finding primary directory name
    d_found = dir_crawl(url, dir_list, random_agent, delay)
    # d_found = dir_crawl(url, dir_list, arg)
    print(f"[*] Discovered Indexable Directory : {d_found}")
    print(f">>> df : {df}")

    # Finding deep directory name -> 모듈화 필요?
    # input : d_found(1차적으로 검색한 dirname), dir_book(디렉토리 이름 파일을 읽은 리스트)
    # output : df(json으로 저장시킬 dic)
    if d_found:
        df = deep_dir_scan(url, d_found, dir_list, random_agent, delay)

    # file discovery
    dir_res = []
    for i in df.keys():
        dir_res.append(i)
        for j in df[i]:
            dir_res.append(i + j)
    print(f"[*] Dir to searching File : {dir_res}")

    try:
        f_found = file_crawl(
            fnm_list, ext_list, url, d_found, dir_res, random_agent, delay, df
        )
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
