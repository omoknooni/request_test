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
    return (
        url,
        word_list,
        max_depth,
        timeout,
        url_set,
        alive_ports,
    )
