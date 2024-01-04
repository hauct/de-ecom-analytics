import pandas as pd
import numpy as np
from time import sleep
import random

from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By

# Set the path to your webdriver
service = Service('chromedriver.exe')

# Initiate the browser
driver = webdriver.Chrome(service=service)

# Open a webpage
driver.get('https://www.lazada.vn/catalog/?_keyori=ss&from=search_history&page=1&q=%C4%91i%E1%BB%87n%20tho%E1%BA%A1i%20di%20%C4%91%E1%BB%99ng&spm=a2o4n.home-vn.search.4.19053bdcPI1FgK&sugg=%C4%91i%E1%BB%87n%20tho%E1%BA%A1i%20di%20%C4%91%E1%BB%99ng_3_1')
sleep(random.randint(5,10))

#================= Get link/title
elems = driver.find_elements(By.CSS_SELECTOR, ".RfADt [href]")
title = [elem.get_attribute('title') for elem in elems]
link = [elem.get_attribute('href') for elem in elems]
print('Got link and title!!!')

#================= Get price
price_elems = driver.find_elements(By.CSS_SELECTOR, ".aBrP0")
price = [elem.text for elem in price_elems]

#================= Table (title, price, link)
df1 = pd.DataFrame(list(zip(title, price, link)), columns=['title', 'price', 'link'])
df1['index'] = np.arange(1, len(df1) + 1)

#================= Get review_number / location
countreview_elems = driver.find_elements(By.CSS_SELECTOR, "._6uN7R")
countreview = [elem.text for elem in countreview_elems]
df1['review_number'] = countreview

#================= Get more information for each item
driver.get(link[0])

name_elems = driver.find_elements(By.CSS_SELECTOR, ".lazyload-wrapper .pdp-mod-review .mod-reviews .middle")
name_comment = [elem.text for elem in name_elems]

content_elems = driver.find_elements(By.CSS_SELECTOR, ".item-content .content")
content_comment = [elem.text for elem in name_elems]

skuinfo_elems = driver.find_elements(By.CSS_SELECTOR, ".item-content .skuInfo")
skuinfo_comment = [elem.text for elem in skuinfo_elems]

likecount_elems = driver.find_elements(By.CSS_SELECTOR, ".item-content .bottom .left .left-content")
likecount_comment = [elem.text for elem in likecount_elems]

df2 = pd.DataFrame(list(zip(name_comment, content_comment, skuinfo_comment, likecount_comment))\
                   , columns=['name_comment', 'content_comment', 'skuinfo_comment', 'likecount_comment'])

df2.insert(0, 'link_item', link[0])

#================= Next pagination
next_pagination_cmt = driver.find_element('xpath', '/html/body/div[4]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]')
next_pagination_cmt.click()

close_btn = driver.find_element('xpath', '/html/body/div[7]/div[2]/div')
close_btn.click()

#=================
count = 0
name_comment, content_comment, skuinfo_comment, likecount_comment = [], [], [], []

while True:
    try:
        print('Check page ' + str(count))    
        name_elems = driver.find_elements(By.CSS_SELECTOR, ".lazyload-wrapper .pdp-mod-review .mod-reviews .middle")
        name_comment = [elem.text for elem in name_elems] + name_comment
        
        content_elems = driver.find_elements(By.CSS_SELECTOR, ".item-content .content")
        content_comment = [elem.text for elem in name_elems] + content_comment
        
        skuinfo_elems = driver.find_elements(By.CSS_SELECTOR, ".item-content .skuInfo")
        skuinfo_comment = [elem.text for elem in skuinfo_elems] + skuinfo_comment
        
        likecount_elems = driver.find_elements(By.CSS_SELECTOR, ".item-content .bottom .left .left-content")
        likecount_comment = [elem.text for elem in likecount_elems] + likecount_comment
        
        