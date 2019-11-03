import pymysql
import time
import pandas as pd
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def into_website(url,url1):
    # 開啟瀏覽器
    browser = webdriver.Chrome()
    # 登入網站
    browser.get(url1)
    # 等待時間
    time.sleep(10)
    # 點擊登入
    elem_login_button = browser.find_element_by_xpath('//*[@id="login_link"]/div')
    elem_login_button.click()
    browser.implicitly_wait(20)
    # 轉進頁框
    iframe = browser.find_element_by_xpath('/html/body/div[7]/div/div/div/iframe')
    browser.switch_to.frame(iframe)
    time.sleep(20)

    # 登入帳號
    elem_usr = browser.find_element_by_xpath('//*[@id="LoginForm_email"]')
    time.sleep(20)
    elem_usr.send_keys(your email)
    # 登入密碼
    elem_pass = browser.find_element_by_xpath('//*[@id="LoginForm_password"]')
    elem_pass.send_keys(your password)
    # 登入
    elem_login = browser.find_element_by_xpath('//*[@id="login-form"]/div[5]/button')
    elem_login.click()
    # 進入目標網頁
    browser.get(url)

def get_buy():
    tablet_buy = browser.find_element_by_xpath("/html/body/div[4]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/table")
    trlist_buy = tablet_buy.find_elements_by_tag_name('tr')
    # [券商名稱,買進,賣出,買超,均價]
    global agent_buy
    agent_buy = []

    for row in trlist_buy:
        tdlist = row.find_elements_by_tag_name('td')
        arr = []
        for col in tdlist:
            arr.append(col.text)
        agent_buy.append(arr)

def get_sell():
    # 獲取表格數據
    tablet_sell = browser.find_element_by_xpath("/html/body/div[4]/div[3]/div[2]/div[2]/div[3]/div[3]/div[2]/div[2]/table")
    # 獲取總行數
    trlist_sell = tablet_sell.find_elements_by_tag_name('tr')
    # [券商名稱,買進,賣出,買超,均價]
    global agent_sell
    agent_sell = []

    for row in trlist_sell:
        tdlist = row.find_elements_by_tag_name('td')
        arr = []
        for col in tdlist:
            arr.append(col.text)
        agent_sell.append(arr)

stockID = input("請輸入你要查詢的股票代號")
date = input("請輸入欲查詢起始時間，格式如2019-09-01")
url1 = "https://www.nvesto.com/"
url = "https://www.nvesto.com/tpe/"+stockID+"/majorForce#!/fromdate/"+date+"/todate/"+date+"/view/summary"

into_website(url,url1)
get_buy()
get_sell()
