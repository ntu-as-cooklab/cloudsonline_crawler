from json import load
from os import makedirs, getcwd, path
from bs4 import BeautifulSoup
import requests
import codecs
import sys
import urllib

# I/O encoding, see https://stackoverflow.com/questions/14630288
if sys.stdout.encoding != 'cp850':
    sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'strict')
if sys.stderr.encoding != 'cp850':
    sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'strict')

with open('page.json') as data_file:
    print ("Loading json..")
    pageLink = load(data_file)

for cloudType in pageLink:
    dic_path = getcwd() + "/photo/" + cloudType
    if not path.isdir(dic_path):
        makedirs(dic_path)
    try:
        link = pageLink[cloudType][0]
        print("Finding all links in: " + link)
        doc = requests.get(link).text
        soup = BeautifulSoup(doc)
        otherLink = soup.find_all('p', align='center')[1].find_all('a')
        link_parts = link.split("/")
        link = ""
        for i in range(len(link_parts)-1):
            link += link_parts[i] + "/"
        for ol in otherLink:
            pageLink[cloudType].append(link + ol["href"])
    except Exception:
        print("Error while making links.")

    print("Start to crawler photos.")
    for link in pageLink[cloudType]:
        try:
            print("Dealing " + link)
            doc = requests.get(link).text
            soup = BeautifulSoup(doc)
            imgLink = soup.find_all('img', width='160')
            for iL in imgLink:
                src = iL["src"]
                src = src.replace("/th/", "/")
                src = src.replace("_th.", ".")
                print("Saving: " + src)
                urllib.urlretrieve(src, dic_path + "/" + src.split("wolken/")[1].split("/")[1])
        except Exception:
            print("Error saving image at link: " + link)