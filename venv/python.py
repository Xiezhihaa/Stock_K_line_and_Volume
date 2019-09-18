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
        global twstockIDint
        twstockIDint = eval(stock_code0)
        return stockIDstring,twstockIDint
    if istwstock== False:
        print("查無代碼")

#國外股票代碼處理
def foreginstock_code(stock_code0):
    return stockIDstring

#時間處理
def date(timedateinput):
    timedate=[]
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
def twstockinformation(stockIDstring,starttime,endtime):
    global df_twstockIDint
    df_twstockIDint= pdr.data.DataReader(stockIDstring, 'yahoo', start=starttime, end=endtime)  # 從yahoo取得歷年股價
    df_twstockIDint.index = df_twstockIDint.index.format(formatter=lambda x: x.strftime("%Y-%m-%d"))

    numberofday = len(df_twstockIDint.index) - 1

    global stock_price
    stock_price = []
    for i in range(numberofday):
        stock_price.append([])
        stock_price[i].append(df_twstockIDint['Open'][i])
        stock_price[i].append(df_twstockIDint['Close'][i])
        stock_price[i].append(df_twstockIDint['Low'][i])
        stock_price[i].append(df_twstockIDint['High'][i])

    global stock_date
    stock_date = []
    for i in range(numberofday):
        stock_date.insert(i, df_twstockIDint.index[i])

    global stock_volume
    stock_volume = []
    for i in range(numberofday):
        stock_volume.append(df_twstockIDint['Volume'][i])
    return stock_price, stock_date, stock_volume,df_twstockIDint

#獲取國外股價資訊
def forgeinstockinformation(stockIDstring,starttime,endtime):
    df_stockIDstring = pdr.data.DataReader(stockIDstring, 'yahoo', start=starttime, end=endtime)  # 從yahoo取得歷年股價
    df_stockIDstring.index = df_twstockIDint.index.format(formatter=lambda x: x.strftime("%Y-%m-%d"))
    return df_stockIDstring, df_stockIDstring.index

#計算移動平均線
def SMA(df_twstockIDint):
    global sma_10, sma_120,sma_240
    sma_10 = talib.SMA(np.array(df_twstockIDint['Close']), 10)
    sma_120 = talib.SMA(np.array(df_twstockIDint['Close']), 120)
    sma_240 = talib.SMA(np.array(df_twstockIDint['Close']), 240)
    return sma_10,sma_120,sma_240

#繪圖
def chart(stock_date,stock_price,sma_10,sma_120,sma_240,stock_volume):
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

    bar=(
        Bar()
        .add_xaxis(stock_date)
        .add_yaxis("交易量", stock_volume,
                    xaxis_index=1, yaxis_index=1, label_opts=opts.LabelOpts(is_show=False),
                    itemstyle_opts=opts.ItemStyleOpts(color="#3B4856", color0="#A73835"),
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

    return grid_chart

#設定參數
yourchoose=input("請選擇你欲查詢股票："
                 "1：臺灣國內股票"
                 "2：國外股票")
stock_code0=input("請輸入你要查詢的股票代號")
starttimeinput=input("請輸入欲查詢起始時間，格式如2019/9/1")
endtimeinput=input("請輸入欲查詢結束時間，格式如2019/9/1")
starttime=date(starttimeinput)
endtime=date(endtimeinput)


twstock_code(stock_code0)
print(stockIDstring)
twstockinformation(stockIDstring,starttime,endtime)
SMA(df_twstockIDint)
grid_chart=chart(stock_date,stock_price,sma_10,sma_120,sma_240,stock_volume)
grid_chart.render()
print(stock_date)

#window.mainloop()
