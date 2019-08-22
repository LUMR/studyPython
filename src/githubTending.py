import csv
import sys

import requests
from bs4 import BeautifulSoup


def getTending(url, params):
    rep = requests.get(url, params)
    bsobj = BeautifulSoup(rep.content, features="lxml")
    csvfile = open('./githubtend.csv', 'w+')
    try:
        writer = csv.writer(csvfile)
        writer.writerow(('user / name', 'url', 'desc', 'stars', 'incr'))
        for art in bsobj.findAll('article', {'class': 'Box-row'}):
            star = art.find('svg', {'aria-label': 'star'}).parent.text.strip()
            newstar = art.findAll('svg', {'class': ['octicon', 'octicon-star'], 'aria-hidden': 'true'})[
                2].parent.text.strip()
            if art.p:
                ps = art.p.text.strip()
            else:
                ps = ''
            print('%s 地址: https://github.com%s \n说明: %s \n星星数:%s 增长数:%s' % (
                art.h1.text.strip(), art.h1.a['href'], ps, star, newstar))
            writer.writerow((art.h1.text.strip(), 'https://github.com' + art.h1.a['href'], ps, star, newstar))
    finally:
        csvfile.close()


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args):
        getTending('https://github.com/trending', {'since': args[0]})
    else:
        getTending('https://github.com/trending', {'since': 'weekly'})
