#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time

url = 'https://www.einvoice.nat.gov.tw/home/Article!showArticleList?articleType=4'
driverPath = r'chromedriver.exe'

with webdriver.Chrome(executable_path=driverPath) as driver:  # ChromeDriver
    driver.get(url)  # 輸入範例網址，交給瀏覽器 
    pageSource = driver.page_source  # 取得網頁原始碼
    # print(driver.name)
    # print(pageSource)

    soup = BeautifulSoup(pageSource, "html5lib")

    bNext = 0 
    for btn in soup.select('.btn-info'):
        if btn.get('onclick') != '':
            bNext = 1

    print(bNext)

    newsUrlList = []

    while bNext>0:
        
        for tag in soup.select('.evn_news-title a'):
            # print(type(str(tag.string)))
            # print(str(tag.string))
            # print(re.sub(r'^\s+', '', str(tag.string)))
            # print(tag.get('href'))
            newsUrlList.append('https://www.einvoice.nat.gov.tw'+tag.get('href'))

        btnNext = driver.find_element_by_xpath('//input[@type="button" and @value="下一頁"]')
        btnNext.click()

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html5lib")

        bNext = 0 
        for btn in soup.select('.btn-info'):
            if btn.get('onclick') and btn.get('value')=='下一頁':
                print (btn.get('onclick'))
                bNext = 1

    print("Info Date, Info Title, Info Content")
    while len(newsUrlList)>0:
        driver.get(newsUrlList.pop(0))
        newsSrc = driver.page_source
        soup = BeautifulSoup(newsSrc, "html5lib")

        infoDate = re.search(r'\d{4}-\d{2}-\d{2}',soup.select_one('.info_date').text).group()
        infoTitle = soup.select_one('.info_title').text
        infoContent = re.sub('\<\w+\>', '',soup.select_one('.info_content').text)

        # print("Info Date: " + infoDate)
        # print("Info Title: " + infoTitle)
        # print("Info Content: " + infoContent)
        print(infoDate + "," + infoTitle + "," + infoContent)

    driver.quit()
