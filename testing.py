from urllib.parse import urlparse


def valid_url(to_validate: str) -> bool:
    o = urlparse(to_validate)
    return True if o.scheme and o.netloc else False


print(valid_url("http://192.168.0.78:80/#./detail.php?id=9'./detail.php?id=10"))
print(valid_url("http://192.168.0.78:80/#./detail.php?id=8'#"))
print(urlparse("http://192.168.0.78:80/#./detail.php?id=9'./detail.php?id=10"))
