def settings(
    mode="default", url="", word_list="", max_depth="", timeout="", alive_ports=""
):
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
    check_set = dict()
    alive_ports = [80, 400]
    return (
        url,
        word_list,
        max_depth,
        timeout,
        check_set,
        alive_ports,
    )
