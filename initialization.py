def init_setting(url, mode, port, max_depth, timeout, word_path):
    # port, max_depth, timeout, word_path
    url = url if url.startswith("http://") else "http://" + url
    word_list = list()
    url_set = dict()
    try:
        with open(word_path, "r") as word_txt:
            for item in word_txt.readlines():
                word_list.append(item.rstrip())
    except Exception as e:
        print("Reading Error : Using Default Words")
        print(e)
        word_list.clear()
        word_list = [
            "",
            "src/",
            "bootstrap/",
            "boards/",
            "css/",
            "js/",
            "admin/",
        ]
    return [url, word_list, max_depth, timeout, url_set, port]
