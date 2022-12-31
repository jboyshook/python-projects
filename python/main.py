import argparse
import subprocess
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.parse import urlparse 
from urllib.request import urlopen
import ssl
import validators
import sys
import re
from exif import Image
import os


parser = argparse.ArgumentParser()
scans = parser.add_mutually_exclusive_group()
scans.add_argument("-iM","--imgs", action = "store_true", required = False, help = "Download all the images in a website")
scans.add_argument("-nM", "--number", action = "store_true", required = False, help = "Extarct all phone numbers")
scans.add_argument('-wM', '--webMap', action = 'store_true', required = False, help = 'Create a web map of all linked sites')
scans.add_argument("-eM", "--emails", action = "store_true", required = False, help = "Extarct email adresses")
scans.add_argument('-gN', '--generalScan', action = 'store_true', required = False, help = 'Run general scan on the website')



parser.add_argument("link", type = str)

args = parser.parse_args()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def download_imgs():
    print("Validating Url......")

    if validators.url(args.link) is True:
        print("Your url has been validated")
    else:
        print("Invalid Url")
        sys.exit()

    print("Downloading Images....")

    url = args.link
    
    html = urlopen(url, context = ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    tags = soup("img")
    imgs_src = []
    for tag in tags:
        imgs_src.append(tag.get("src", None))
    
    linked_srcs = []
    unlinked_srcs = []
    for i in imgs_src:
        if url_validator(i) is True:
            linked_srcs.append(i)
        elif url_validator(i) is False:
            unlinked_srcs.append(i)
        else:
            print("An unexpected error occured")

    parsed_url = urlparse(args.link)
    main_url = parsed_url.scheme + "://" + parsed_url.hostname #type:ignore

    for link in linked_srcs:
        subprocess.call(["wget", str(link)])
    for li in unlinked_srcs:
        subprocess.call(["wget", str(main_url) + str(li)])
    
    print("Enter yes or no, all in small")
    exif_prompt = str(input("Do you want to extract the exif data from the images: "))
    if exif_prompt == "yes":
        exif_data()

    elif exif_prompt == "no":
        print("Exiting....")
        sys.exit()
    
    else:
        print("Invalid Input")

def url_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

        
def exif_data():
    all_files  = os.listdir()
    images = []
    for i in all_files:
        if i[-4:] == ".jpg" or i[-4:] == ".png":
            images.append(i)
        
    for img in images:
        with open(str(img), 'rb') as image_file:
            my_image = Image(image_file)
        print("Data of image:", img)
        print(my_image.get_all())

def extract_emails():
    print("Validating Url......")
    if validators.url(args.link) == True:
        print("Your url has been validated")
    else:
        print("Invalid Url")
        sys.exit()

    url = args.link
    html = urlopen(url, context = ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    url_text = soup.get_text()
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", url_text)

    print("All your extracted emails are:")
    print(emails)

def extract_numbers():
    print("Validating Url......")
    if validators.url(args.link) == True:
        print("Your url has been validated")
    else:
        print("Invalid Url")
        sys.exit()

    url = args.link
    html = urlopen(url, context = ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    url_text = soup.get_text()
    numbers = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', url_text)

    print("All your extracted numbers are:")
    print(numbers)

def webMap(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    tags = soup('a')
    links = []

    for tag in tags:
        links.append(tag.get('href', None))
    

    parsed_url = urlparse(url)
    main_url = parsed_url.scheme + "://" + parsed_url.hostname #type:ignore

    interdomain_links = []
    exterdomain_links = []
    for i in links:
        if url_validator(i) is True:
            exterdomain_links.append(i)
        elif url_validator(i) is False:
            interdomain_links.append(main_url+i)
        else:
            print("An unexpected error occured")
    
    
    all_links = []
    for link in interdomain_links:
        all_links.append(link)
    for link in exterdomain_links:
        all_links.append(link)

    
    with open(r'output.txt', 'a') as fp:
        for link in all_links:
            fp.write("%s\n" % link)
    
    try:
        while len(all_links) > 0:
            for i in all_links:
                webMap(i)
    except HTTPError:
         print('Too Many request')
         sys.exit()



        
if args.imgs:
    download_imgs()
elif args.emails:
    extract_emails()
elif args.number:
    extract_numbers()
elif args.webMap:
    webMap(args.link)
else:
    #add exit prompt later
    sys.exit()
