import os

from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
userAgent = ua.random
print(type(userAgent))
print(os.getcwd())
print(os.path.join(os.getcwd(), "/reports/"))
print(os.listdir())