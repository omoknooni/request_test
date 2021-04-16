import argparse
from initialization import settings2
from scan import main_scan
from report import initial_report, final_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Enter URL or Domain to Inspect")
    parser.add_argument(
        "-mode",
        default="default",
        help="Enter custom to configure port, max_depth, etc..",
    )
    parser.add_argument("-port", default=80, help="Enter PORT to inspect e.g) 80, 8080")
    parser.add_argument("-max_depth", default=3, help="Enter max-depth to use")
    parser.add_argument(
        "-timeout", default=0.5, help="Enter maximum timeout for each connection"
    )
    parser.add_argument(
        "-word_path",
        default="word_list",
        help="Enter your word_list.txt path.",
    )
    args = parser.parse_args()
    return args


def get_settings(args):
    args.word_path = "./config/" + args.word_path + ".txt"
    conf = settings2(
        url=args.url,
        mode=args.mode,
        port=args.port,
        max_depth=args.max_depth,
        timeout=args.timeout,
        word_path=args.word_path,
    )
    return conf


if __name__ == "__main__":
    print("[1] : Parsing Arguments")
    args = main()
    print("[1] :Done")

    print("[2] : Loading Settings from parsed Arguments")
    conf = get_settings(args)
    print("[2] : Done")
    
    initial_result, total_result = main_scan(conf)
    # make reports
