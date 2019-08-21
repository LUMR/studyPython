#!/usr/bin/env python3

from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver,common

urlopen = request.urlopen


# 实例1
def cnblogs():
    html = urlopen('https://www.cnblogs.com/Lijcyy/p/9778318.html')
    bsobj = BeautifulSoup(html, features="lxml")
    postList = bsobj.findAll('div', {'class': 'postBody'})
    for post in postList:
        print(post)


def cna():
    html = urlopen("https://www.cnblogs.com/Lijcyy/p/9778318.html")
    bsobj = BeautifulSoup(html, features="lxml")
    # for link in bsobj.findAll('a'):
    #     if 'href' in link.attrs:
    #         print(link.attrs['href'])
    print(bsobj)


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs',{
        'profile.default_content_settings': {
            'images': 2
        },
        'profile.managed_default_content_settings': {
            'images': 2
        }
    })
    # options.headless = True
    # options.add_argument('--disable-gpu')
    broswer = webdriver.Chrome(executable_path='/Users/meicloud/apps/bin/chromedriver', chrome_options=options)
    try:
        broswer.get('https://www.cnblogs.com/Lijcyy/p/9778318.html')
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
    except common.exceptions.TimeoutException:
        broswer.execute_script('window.stop()')
