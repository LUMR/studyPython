#!/usr/bin/env python3
import csv
import sys
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver, common


def createBrowser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        'profile.default_content_settings': {
            'images': 2
        },
        'profile.managed_default_content_settings': {
            'images': 2
        }
    })
    return webdriver.Chrome(executable_path='$HOME/apps/bin/chromedriver', chrome_options=options)


def search():
    url = 'https://www.lagou.com/zhaopin/Java/'
    browser = createBrowser()
    browser.get('%s%s' % (url, ''))
    rs = browser.find_element_by_class_name('city-wrapper')
    rs.find_element_by_link_text('广州').click()
    sleep(5)
    rs = browser.find_element_by_id('switchCity')
    rs.find_element_by_link_text('广州站').click()
    sleep(5)
    for i in list(range(29)):
        browser.get('%s%s' % (url, str(i + 1)))
        sleep(6)
        ansyHtml(browser.page_source, i)
        sleep(5)
    browser.quit()


def ansyHtml(source, i):
    html = BeautifulSoup(source, features='lxml')
    list = html.find('div', {'id': 's_position_list'}).ul.findAll('li')
    with open('$HOME/Local/lagou_%s.html' % str(i), 'w+') as f:
        f.write(source)
    print('打印第%s页完成' % str(i + 1))


if __name__ == '__main__':
    search()
