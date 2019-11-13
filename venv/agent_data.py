import pymysql
import time
import pandas as pd
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def into_website(url,url1):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # 開啟瀏覽器
    browser = webdriver.Chrome(chrome_options=chrome_options)
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
    elem_usr.send_keys("nagi30912@gmail.com")
    # 登入密碼
    elem_pass = browser.find_element_by_xpath('//*[@id="LoginForm_password"]')
    elem_pass.send_keys("Python404220008")
    # 登入
    elem_login = browser.find_element_by_xpath('//*[@id="login-form"]/div[5]/button')
    elem_login.click()
    # 進入目標網頁
    browser.get(url)

    return browser

def get_buy(browser):
    tablet_buy = browser.find_element_by_xpath("/html/body/div[4]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/table")
    trlist_buy = tablet_buy.find_elements_by_tag_name('tr')
    # [券商名稱,買進,賣出,買超,均價]
    global agent_buy
    agent_buy = []

    for i in range(len(trlist_sell)):
        a=str(i+1)
        xpath='/html/body/div[4]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/table/tbody/tr['+a+']/td[1]/a'
        browser.find_element_by_xpath(xpath).click()
        time.sleep(20)
        browser.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[2]/div[8]/div[1]/div[3]/div[2]/button[3]').click()
        table_buy = browser.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody')
        trlist_buy = table_buy.find_elements_by_tag_name('tr')
        for row in trlist_buy:
            tdlist = row.find_elements_by_tag_name('td')
            arr=[]
            for col in tdlist:
                arr.append(col.text)
            agent_buy.append(arr)
        browser.get(url)
        time.sleep(20)

    return agent_buy

def get_sell(browser):
    # 獲取表格數據
    tablet_sell = browser.find_element_by_xpath("/html/body/div[4]/div[3]/div[2]/div[2]/div[3]/div[3]/div[2]/div[2]/table")
    # 獲取總行數
    trlist_sell = tablet_sell.find_elements_by_tag_name('tr')
    # [券商名稱,買進,賣出,買超,均價]
    global agent_sell
    agent_sell = []

    global agent
    agent=[]

    for row in trlist_sell:
        tdlist = row.find_elements_by_tag_name('td')
        arr = []
        for col in tdlist:
            arr.append(col.text)
        agent_sell.append(arr)

    return agent_sell

#資料庫
def get_conn_db():
    try:
        db = pymysql.connect(host='127.0.0.1',user='root',passwd='404220008',db="stock_test",port=3306,charset='utf8mb4')
    except pymysql.Error as e:
        print(e)
        print("連接資料庫失敗")

def close_conn_db():
    try:
        if db.conn:
            db.close()
    except pymysql.Error as e:
        print(e)
        print("關閉資料庫失敗")

def add_data():
    sql = 'INSERT INTO'
    try:
        db.get_conn_db()
        cursor = db.conn.cursor()
        cursor.execute(sql,)
        db.conn.commit()
        return 1
    except AttributeError as e:
        print('Error:',e)
        return 0
    except TypeError as e:
        print('Error:',e)
        db.conn.commit()
        db.conn.rollback()
        return 0
    finally:
        cursor.close()
        db.close_conn_db()

#執行
stockID = input("請輸入你要查詢的股票代號")
date = input("請輸入欲查詢起始時間，格式如2019-09-01")
url1 = "https://www.nvesto.com/"
url = "https://www.nvesto.com/tpe/"+stockID+"/majorForce#!/fromdate/"+date+"/todate/"+date+"/view/summary"

browser=into_website(url,url1)
agent_buy = get_buy(browser)
agent_sell = get_sell(browser)

#[日期,買進,比例,賣出,比例,買賣超,近一週.....]
