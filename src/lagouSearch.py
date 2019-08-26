#!/usr/bin/env python3
import csv
import sys
from time import sleep

import requests
from bs4 import BeautifulSoup, element
from selenium import common, webdriver


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
    return webdriver.Chrome(executable_path='/Users/meicloud/apps/bin/chromedriver', options=options)


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
    for i in list(range(30)):
        browser.get('%s%s' % (url, str(i + 1)))
        sleep(6)
        ansyHtml(browser.page_source, i)
        sleep(5)
    browser.quit()


def ansyHtml(source, i):
    html = BeautifulSoup(source, features='lxml')
    lis = html.find('div', {'id': 's_position_list'}).ul.findAll('li')
    for li in lis:
        industry = li.find('div', {'class': 'industry'}).text.strip()
        tag = li.find('div', {'class': 'li_b_r'}).text.strip()
        require = li.find('span', {'class': 'money'}
                          ).parent.contents[4].strip()
        link = li.find('a', {'class': 'position_link'})['href']
        info = li.attrs.copy()
        info['industry'] = industry
        info['tag'] = tag
        info['require'] = require
        info['link'] = link
        saveResult(info)


def ansyLocal():
    for i in list(range(29)):
        with open('/Users/meicloud/Local/lagou_%s.html' % str(i), 'r') as f:
            html = BeautifulSoup(f.read(), features='lxml')
            lis = html.find('div', {'id': 's_position_list'}).ul.findAll('li')
            for li in lis:
                industry = li.find('div', {'class': 'industry'}).text.strip()
                tag = li.find('div', {'class': 'li_b_r'}).text.strip()
                require = li.find('span', {'class': 'money'}
                                  ).parent.contents[4].strip()
                link = li.find('a', {'class': 'position_link'})['href']
                info = li.attrs.copy()
                info['industry'] = industry
                info['tag'] = tag
                info['require'] = require
                info['link'] = link
                print(info)
                saveResult(info)


num = 1


def saveResult(result):
    global num
    resp = requests.post('http://localhost:9200/works/_doc/%s' % str(num), json=result)
    print(resp)
    num = num + 1


if __name__ == '__main__':
    # ansyLocal()
    search()