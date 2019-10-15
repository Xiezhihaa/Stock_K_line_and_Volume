#引入數據庫
from pyecharts.charts import Kline
from pyecharts.charts import Line
from pyecharts.charts import Bar
from pyecharts.charts import Grid
from pyecharts import options as opts
import pandas_datareader as pdr
import pandas_datareader.data as web
import mpl_finance as mpf
import numpy as np          #匯入陣列套件
import pandas as pd         #匯入
import seaborn as sns       #匯入視覺化模組
import datetime as datetime
import tkinter as tk
import talib                #匯入金融模塊
import twstock
open('python.py',encoding='windows-1252')

#設定視窗
#window=tk.Tk()
#window.title('My Stock Kline Chart')
#window.geometry('500x300')
#宣告函數
#臺灣股票代碼處理
def twstock_code(stock_code0):
    istwstock=stock_code0 in twstock.codes
    if istwstock == True:
        global stockIDstring
        stockIDstring = stock_code0 + '.TW'
        global stockIDint
        stockIDint = eval(stock_code0)
        return stockIDstring,stockIDint
    if istwstock== False:
        print("查無代碼")

#國外股票代碼處理
def foreginstock_code(stock_code0):
    global stockIDstring
    global stockIDint
    stockIDstring = stock_code0
    stockIDint = stock_code0
    return stockIDstring

#時間處理
def date(timedateinput):
    timedate=[]
    global timeoutput
    timedate=timedateinput.split('/')

    year=eval(timedate[0])
    month=eval(timedate[1])
    day=eval(timedate[2])
    if month in range(1,12):
        if day in range(1,31):
            timeoutput=datetime.datetime(year,month,day)
        else:
            print("你輸入的日期格式有誤")
    return timeoutput

# 獲取臺灣股票資訊
def stockinformation(stockIDstring,starttime,endtime):
    global df_stockIDint
    df_stockIDint= pdr.data.DataReader(stockIDstring, 'yahoo', start=starttime, end=endtime)  # 從yahoo取得歷年股價
    df_stockIDint.index = df_stockIDint.index.format(formatter=lambda x: x.strftime("%Y-%m-%d"))

    numberofday = len(df_stockIDint.index) - 1

    global stock_price
    stock_price = []
    for i in range(numberofday):
        stock_price.append([])
        stock_price[i].append(df_stockIDint['Open'][i])
        stock_price[i].append(df_stockIDint['Close'][i])
        stock_price[i].append(df_stockIDint['Low'][i])
        stock_price[i].append(df_stockIDint['High'][i])

    global stock_date
    stock_date = []
    for i in range(numberofday):
        stock_date.insert(i, df_stockIDint.index[i])

    global stock_volume_red
    global stock_volume_green
    global stock_volume_gray
    stock_volume_red = [0]
    stock_volume_green = [0]
    stock_volume_gray = []
    stock_volume_gray.append(df_stockIDint['Volume'][0])

    for i in range(numberofday):
        if df_stockIDint['Close'][i+1]>df_stockIDint['Close'][i]:
            stock_volume_red.append(df_stockIDint['Volume'][i+1])
        else:
            stock_volume_red.append(0.00)

    for i in range(numberofday):
        if df_stockIDint['Close'][i+1]<df_stockIDint['Close'][i]:
            stock_volume_green.append(df_stockIDint['Volume'][i + 1])
        else:
            stock_volume_green.append(float(0))

    for i in range(numberofday):
        if df_stockIDint['Close'][i+1]==df_stockIDint['Close'][i]:
            stock_volume_gray.append(df_stockIDint['Volume'][i + 1])
        else:
            stock_volume_gray.append(float(0))

    return stock_price, stock_date, stock_volume_red,stock_volume_green,stock_volume_gray,df_stockIDint

#計算移動平均線
def SMA():
    global sma_10, sma_120,sma_240
    sma_10 = talib.SMA(np.array(df_stockIDint['Close']), 10)
    sma_120 = talib.SMA(np.array(df_stockIDint['Close']), 120)
    sma_240 = talib.SMA(np.array(df_stockIDint['Close']), 240)
    return sma_10,sma_120,sma_240

#繪圖
def chart():
    kline=(
        Kline()
        .add_xaxis(stock_date)
        .add_yaxis("Kline", stock_price)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                # 顯示分割
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),

            # 圖例位置
            legend_opts=opts.LegendOpts(is_show=True, pos_top=10, pos_left="center"),
            # DataZoom slider
            datazoom_opts=[opts.DataZoomOpts(is_show=False, type_="inside",
                                             xaxis_index=[0, 1], range_start=0, range_end=100, ),
                           opts.DataZoomOpts(is_show=True, xaxis_index=[0, 1], type_="slider",
                                             pos_top="90%", range_start=0, range_end=100, )],

            tooltip_opts=opts.TooltipOpts(
                trigger="axis", axis_pointer_type="cross", background_color="rgba(245,245,245,0.8)",
                border_width=1, border_color="#ccc", textstyle_opts=opts.TextStyleOpts(color="#000")
            ),

            # axispointer_opts.AxisPointerOpts(is_show=True,link=[{"xAxisIndex":"all"}],
            # label=opts.LabelOpts(background_color=''#777'),),

            # 區域選擇組件
            # brush_opts=opts.BrushOpts(#指定所有數列對應的座標系x_axis_index="all",#指定哪些 series
            # 可以被聯動brush_link="all",#定義顏色透明度out_of_brush={"colorAlpha":0.1},brush_type="lineX",),

        )
    )

    line=(
        Line()
        .add_xaxis(stock_date)
        .add_yaxis("10日移動平均線", sma_10, is_smooth=True,
                    label_opts=opts.LabelOpts(is_show=False),
                    linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5))
        .add_yaxis("120日移動平均線", sma_120, is_smooth=True,
                    label_opts=opts.LabelOpts(is_show=False),
                    linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5))
        .add_yaxis("240日移動平均線", sma_240, is_smooth=True,
                    label_opts=opts.LabelOpts(is_show=False),
                    linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5))
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(type_="category"),
        )
    )

    bar = (
        Bar()
            .add_xaxis(stock_date)
            .add_yaxis("交易量", stock_volume_red, gap="0%",
                       xaxis_index=1, yaxis_index=1, label_opts=opts.LabelOpts(is_show=False),
                       itemstyle_opts=opts.ItemStyleOpts(color="#A73835"),
                       )
            .add_yaxis("交易量", stock_volume_green,gap="0%",
                       xaxis_index=1, yaxis_index=1, label_opts=opts.LabelOpts(is_show=False),
                       itemstyle_opts=opts.ItemStyleOpts(color="#424A56"),
                       )
            .add_yaxis("交易量", stock_volume_gray,gap="0%",
                       xaxis_index=1, yaxis_index=1, label_opts=opts.LabelOpts(is_show=False),
                       itemstyle_opts=opts.ItemStyleOpts(color="#404143")
                       )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(type_="category", is_scale=True, grid_index=1, boundary_gap=False,
                                     axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                                     axistick_opts=opts.AxisTickOpts(is_show=False),
                                     splitline_opts=opts.SplitLineOpts(is_show=False),
                                     axislabel_opts=opts.LabelOpts(is_show=False),
                                     split_number=20, ),
            yaxis_opts=opts.AxisOpts(grid_index=1, is_scale=True, split_number=2,
                                     axislabel_opts=opts.LabelOpts(is_show=False),
                                     axisline_opts=opts.AxisLineOpts(is_show=False),
                                     axistick_opts=opts.AxisTickOpts(is_show=False),
                                     ),

            legend_opts=opts.LegendOpts(is_show=False),

        )
    )


    overlap_kline_line = kline.overlap(line)

    global grid_chart

    grid_chart = (
        Grid()
        .add(overlap_kline_line,
             grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
             )
        .add(bar,
             grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", pos_top="70%", height="16%"), )
    )

    grid_chart.render()


#設定參數
yourchoose=input("請選擇你欲查詢股票："
                 "1：臺灣國內股票"
                 "2：國外股票")
if yourchoose=="1" or "2":
    stock_code0 = input("請輸入你要查詢的股票代號")
    starttimeinput = input("請輸入欲查詢起始時間，格式如2019/9/1")
    endtimeinput = input("請輸入欲查詢結束時間，格式如2019/9/1")
    starttime = date(starttimeinput)
    endtime = date(endtimeinput)

    if yourchoose=="1":
        twstock_code(stock_code0)
        stockinformation(stockIDstring, starttime, endtime)
        SMA()
        chart()
    elif yourchoose == '2':
        foreginstock_code(stock_code0)
        stockinformation(stockIDstring, starttime, endtime)
        SMA()
        chart()
else:
    print("請輸入數字 1 與 2")

#window.mainloop()
