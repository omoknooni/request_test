import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Enter URL or Domain to Inspect")
    parser.add_argument(
        "--port", nargs="?", default=80, help="Enter PORT to inspect e.g) 80, 8080"
    )
    args = parser.parse_args()
    print(args)
    url = args.url
    port = args.port
    print(url)
    print(port)


if __name__ == "__main__":
    main()