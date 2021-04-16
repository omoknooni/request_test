def settings(
    mode="default", url="", word_list="", max_depth="", timeout="", alive_ports=""
):
    # Custom Settings
    if mode == "default":
        url = "http://192.168.0.78"
        word_list = [
            "",
            "src/",
            "bootstrap/",
            "boards/",
            "css/",
            "js/",
            "admin/",
        ]
        timeout = 0.5
        max_depth = 3
    # Default Variables
    url_set = dict()
    alive_ports = [80, 400]
    return [
        url,
        word_list,
        max_depth,
        timeout,
        url_set,
        alive_ports,
    ]


def settings2(url, mode, port, max_depth, timeout, word_path):
    # port, max_depth, timeout, word_path
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
