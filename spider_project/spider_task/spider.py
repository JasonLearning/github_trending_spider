#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/5 下午1:34
# @Author  : Jason
# @Site    : 
# @File    : spider.py

import datetime
import codecs
import requests
import os
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, InvalidSelectorException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def git_add_commit_push(date, filename):
    cmd_git_add = 'git add {filename}'.format(filename=filename)
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)


def create_markdown(date, filename):
    with open(filename, 'w') as f:
        f.write("##-*-" + date + "-*-\n")


def scrape(language, filename):
    driver = webdriver.PhantomJS()
    url = 'https://github.com/trending/{language}'.format(language=language)
    driver.get(url)

    items = driver.find_elements_by_xpath('//*[@class="repo-list"]/li')
    with codecs.open(filename, "a", "utf-8") as f:
        f.write('\n####{language}\n'.format(language=language))
        for i in items:
            url = i.find_element_by_xpath("./div/h3/a").get_attribute('href')
            title = url[19:]
            description = i.find_element_by_xpath("./div[3]/p").text
            f.write(u"* [{title}]({url}):{description}\n".format(title=title, url=url, description=description))


def job():

    str_date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=str_date)

    create_markdown(str_date, filename)

    scrape('python', filename)
    scrape('go', filename)

    # git add commit push
    git_add_commit_push(str_date, filename)


if __name__ == '__main__':
    # while True:
        job()
    #     time.sleep(24 * 60 * 60)
    # scrape("python")
