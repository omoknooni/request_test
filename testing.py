from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
userAgent = ua.random
print(type(userAgent))
