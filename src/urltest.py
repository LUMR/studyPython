#!/usr/bin/env python3

from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver, common
from time import sleep
import requests
import csv

urlopen = request.urlopen


# 实例1
def cnblogs():
    html = urlopen('https://www.cnblogs.com/Lijcyy/p/9778318.html')
    bsobj = BeautifulSoup(html, features="lxml")
    postList = bsobj.findAll('div', {'class': 'postBody'})
    for post in postList:
        print(post)


def cna(url):
    html = urlopen(url)
    bsobj = BeautifulSoup(html, features="lxml")
    for link in bsobj.findAll('a'):
        if 'href' in link.attrs:
            print(link.attrs['href'])


def seleniumtest():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        'profile.default_content_settings': {
            'images': 2
        },
        'profile.managed_default_content_settings': {
            'images': 2
        }
    })
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 切换到开发者模式
    # options.headless = True
    # options.add_argument('--disable-gpu')
    broswer = webdriver.Chrome(executable_path='/Users/meicloud/apps/bin/chromedriver', chrome_options=options)
    try:
        broswer.get('https://www.zhihu.com/topic/19574589/hot')
        sleep(20)

        broswer.execute_script('window.open()')
        broswer.switch_to.window(broswer.window_handles[1])
        broswer.get('https://www.baidu.com')
        broswer.switch_to.window(broswer.window_handles[0])
        bsobj = BeautifulSoup(broswer.page_source, features="lxml")
        print('页面加载完成')

        broswer.quit()
        for link in bsobj.findAll('a'):
            if 'href' in link.attrs:
                print(link.attrs['href'])
            print(link.text)
    except common.exceptions.TimeoutException:
        broswer.execute_script('window.stop()')


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
    getTending('https://github.com/trending', {'since': 'weekly'})
