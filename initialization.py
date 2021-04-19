import typing
import os


def read_file(workfolder, filename):
    token_list = list()
    token_path = os.path.join(workfolder, filename)
    print("Reading file from : ", token_path)
    try:
        with open(token_path, "r") as word_txt:
            for item in word_txt.readlines():
                token_list.append(item.rstrip())
    except Exception as e:
        # other error handling for file I/O
        print(e)
    return token_list


def init_setting(
    url: str,
    port: int,
    max_depth: int,
    timeout: float,
    delay: float,
    random_agent: bool,
    request_delay: bool,
    config_folder: str,
    report_folder: str,
    word_path: str,
    dir_path: str,
    fnm_path: str,
    ext_path: str,
) -> list:
    # port, max_depth, timeout, word_path
    url = url if url.startswith("http://") else "http://" + url
    word_list = list()
    dir_list = list()
    fnm_list = list()
    ext_list = list()

    url_set = dict()

    word_list = read_file(config_folder, word_path)
    dir_list = read_file(config_folder, dir_path)
    fnm_list = read_file(config_folder, fnm_path)
    ext_list = read_file(config_folder, ext_path)

    # return REQUIRED DATA ONLY (which required for afterwards)
    return [
        url,
        port,
        max_depth,
        timeout,
        delay,
        random_agent,
        request_delay,
        report_folder,
        word_list,
        dir_list,
        fnm_list,
        ext_list,
        url_set,
    ]
