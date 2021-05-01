import requests
from bs4 import BeautifulSoup

def getIFunnyMediaLink(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser')
    item = soup.find_all('li',{'class':'stream__item'})[0].find_all('div',{'class':'media'})[0]
    mediaLink = ''
    if '.mp4' not in str(item):
        item = item.findChildren('div')[0].findChildren('div')[0].findChildren()[0]
    for i in ['data-src', 'data-source']:
        if i in item.attrs:
            mediaLink = item[i]
            break

    return mediaLink
