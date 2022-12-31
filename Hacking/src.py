from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import subprocess

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

subprocess.call(["touch", "output.txt"])

url = "https://www.instagram.com/namanjaiswal/"
html = urlopen(url, context = ctx).read()
bsObj = BeautifulSoup(html, "html.parser")

with open("output.txt", "w") as file:
    file.write(bsObj.prettify())
