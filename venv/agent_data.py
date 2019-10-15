#匯入庫
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#基本參數
stockID = input("請輸入你要查詢的股票代號")
date = input("請輸入欲查詢起始時間，格式如2019-09-01")
url1 = "https://www.nvesto.com/"
url = "https://www.nvesto.com/tpe/"+stockID+"/majorForce#!/fromdate/"+date+"/todate/"+date+"/view/summary"

#開啟瀏覽器
browser = webdriver.Chrome()
#登入網站
browser.get(url1)
#等待時間
time.sleep(10)

#點擊登入
elem_login = browser.find_element_by_xpath('//*[@id="login_link"]/div')
elem_login.click()
browser.implicitly_wait(10)

#轉進頁框
browser.switch_to.frame("fancybox-frame1571105650798")
browser.switch_to.frame("fancybox-frame1571106072018")
#登入帳號
elem_usr = browser.find_element_by_xpath('//*[@id="LoginForm_email"]')
elem_usr.send_keys("you email")
#登入密碼
elem_pass = browser.find_element_by_xpath('//*[@id="LoginForm_password"]')
elem_pass.send_keys("your password")
#登入
elem_send = browser.find_element_by_xpath('//*[@id="login-form"]/div[5]/button')
elem_send.click()
#進入目標網頁
browser.get(url)

#獲取表格資料
tablet = browser.find_element_by_class_name("/html/body/div[4]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]")
trlist = browser.find_elements_by_tag_name('tr')

#會出現大量不需要資料，待解決
for row in trlist:
    tdlist = row.find_elements_by_tag_name('td')
    for col in tdlist:
        print(col.text+'\t',end='')


#將表格資料匯入
#獲取表格資料 SQL
