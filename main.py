# Python Module
import argparse
import typing

# Custom Module
import initialization
import scan
import report


def main() -> list:
    parser = argparse.ArgumentParser(
        description="Directory checking tool as a web scanning, random-agent option and random-delay option is recommanded"
    )
    parser.add_argument("url", help="Enter URL or Domain to Inspect")
    parser.add_argument("-port", default=80, help="Enter PORT to inspect e.g) 80, 8080")
    parser.add_argument("-max_depth", default=3, help="Enter max-depth to use")
    parser.add_argument(
        "-timeout", default=0.5, help="Enter maximum timeout for each connection"
    )
    parser.add_argument(
        "-d",
        help="Add delay between requests, default value is 1",
        dest="delay",
        type=float,
        default=1,
    )
    parser.add_argument(
        "-ra",
        help="Enable RandomAgent mode",
        dest="random_agent",
        required=False,
        default=True,
    )
    parser.add_argument(
        "-rt",
        help="Enable Random request dealy mode",
        dest="request_delay",
        required=False,
        default=True,
    )
    parser.add_argument(
        "-report",
        help="A specific Folder to Store JSON reports",
        dest="report_folder",
        type=str,
        required=False,
        default="reports",
    )
    parser.add_argument(
        "-config",
        help="A Specific Folder to Load your config files : name_book, word_path etc..",
        dest="config_folder",
        type=str,
        required=False,
        default="configs",
    )
    parser.add_argument(
        "-w",
        dest="word_path",
        default="word_list.txt",
        type=str,
        required=False,
        help="A specific path to word_list file",
    )
    parser.add_argument(
        "-l",
        help="A specific path to dir_list file",
        dest="dir_path",
        type=str,
        required=False,
        default="dir_book.txt",
    )
    parser.add_argument(
        "-f",
        help="A specific path to filename_list file",
        dest="fnm_path",
        type=str,
        required=False,
        default="name_book.txt",
    )
    parser.add_argument(
        "-e",
        help="A specific path to extenion_list file",
        dest="ext_path",
        type=str,
        required=False,
        default="extension_book.txt",
    )
    args = parser.parse_args()
    return args


def get_settings(args: list) -> list:
    conf = initialization.init_setting(
        url=args.url,
        port=args.port,
        max_depth=args.max_depth,
        timeout=args.timeout,
        delay=args.delay,
        random_agent=args.random_agent,
        request_delay=args.request_delay,
        config_folder=args.config_folder,
        report_folder=args.report_folder,
        word_path=args.word_path,
        dir_path=args.dir_path,
        fnm_path=args.fnm_path,
        ext_path=args.ext_path,
    )
    return conf


if __name__ == "__main__":
    print("[1] : Parsing Arguments")

    args = main()

    print("[1] :Done")

    print("[2] : Loading Settings from parsed Arguments")

    conf = get_settings(args)
    print(conf)
    url = conf[0]

    print("[2] : Done")
    print("[3] : Start Scanning according to settings")

    initial_result, final_result = scan.scan_entry(conf)

    print("[3] : Done")
    print("[4] : Making Reports")

    # make reports
    report.make_report(initial_result, "initial")
    report.make_report(final_result, "final")
    print("[4] : All DONE! Check ./report/ ")
