import ssl
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://sidbi.in/en"

html = urlopen(url, context = ctx).read()
soup = BeautifulSoup(html, 'html.parser')

tags = soup('a')
hrefs = []
products = []
for tag in tags:
    hrefs.append(tag.get("href", None))

for href in hrefs:
    if "products#" in href:
        products.append(href)

for product in products:
    html = urlopen(product, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    with open('sidbi.txt', 'a') as file:
        file.write(soup.get_text())
print(products)