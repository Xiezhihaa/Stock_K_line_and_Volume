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
import talib                #匯入金融模塊
import twstock
open('python.py',encoding='windows-1252')

#設定參數
yourchoose=input("請選擇你欲查詢股票："
                 "1：臺灣國內股票"
                 "2：國外股票")
stock_code0=input("請輸入你要查詢的股票代號")
stock_code1=stock_code0+'.TW'
stock_code2=eval(stock_code0)

start=datetime.datetime(2019,1,1)
endtime=datetime.datetime(2019,9,1)
df_stock_code2=pdr.data.DataReader(stock_code1,'yahoo',start=start,end=endtime) #從yahoo取得歷年股價
df_stock_code2.index=df_stock_code2.index.format(formatter=lambda x:x.strftime("%Y-%m-%d")) #lambda函數，datetime 轉成字

#轉換成陣列
numberofday=len(df_stock_code2.index)-1
stock_price=[]
for i in range(numberofday):
    stock_price.append([])
    stock_price[i].append(df_stock_code2['Open'][i])
    stock_price[i].append(df_stock_code2['Close'][i])
    stock_price[i].append(df_stock_code2['Low'][i])
    stock_price[i].append(df_stock_code2['High'][i])

stock_date=[]
for i in range(numberofday):
    stock_date.insert(i, df_stock_code2.index[i])

#獲取移動平均線資訊
sma_10 = talib.SMA(np.array(df_stock_code2['Close']), 10)
sma_120 = talib.SMA(np.array(df_stock_code2['Close']), 120)
sma_240 = talib.SMA(np.array(df_stock_code2['Close']), 240)

#獲取交易日資訊
stock_volume=[]
for i in range(numberofday):
    stock_volume.append(df_stock_code2['Volume'][i])

#繪畫K線圖
kline=(
    Kline()
    .add_xaxis(stock_date)
    .add_yaxis("Kline",stock_price)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            #顯示分割
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),

        #圖例位置
        legend_opts=opts.LegendOpts(is_show=True,pos_top=10,pos_left="center"),
        #DataZoom slider
        datazoom_opts=[opts.DataZoomOpts(is_show=False, type_="inside",
                                         xaxis_index=[0, 1], range_start=0, range_end=100, ),
                       opts.DataZoomOpts(is_show=True, xaxis_index=[0, 1], type_="slider",
                                         pos_top="90%", range_start=0, range_end=100, )],

        tooltip_opts=opts.TooltipOpts(
            trigger="axis", axis_pointer_type="cross",background_color="rgba(245,245,245,0.8)",
            border_width=1, border_color="#ccc", textstyle_opts=opts.TextStyleOpts(color="#000")
        ),

        #axispointer_opts.AxisPointerOpts(is_show=True,link=[{"xAxisIndex":"all"}],
        # label=opts.LabelOpts(background_color=''#777'),),

        #區域選擇組件
        #brush_opts=opts.BrushOpts(#指定所有數列對應的座標系x_axis_index="all",#指定哪些 series
        # 可以被聯動brush_link="all",#定義顏色透明度out_of_brush={"colorAlpha":0.1},brush_type="lineX",),

    )
)

#繪畫移動平均線
line=(
    Line()
    .add_xaxis(stock_date)
    .add_yaxis("10日移動平均線",sma_10,is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False),
               linestyle_opts=opts.LineStyleOpts(width=3,opacity=0.5))
    .add_yaxis("120日移動平均線",sma_120,is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False),
               linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5))
    .add_yaxis("240日移動平均線",sma_240,is_smooth=True,
               label_opts=opts.LabelOpts(is_show=False),
               linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5))
    .set_global_opts(
            xaxis_opts=opts.AxisOpts(type_="category"),
        )
)

bar=(
    Bar()
    .add_xaxis(stock_date)
    .add_yaxis("交易量",stock_volume,
               xaxis_index=1,yaxis_index=1,label_opts=opts.LabelOpts(is_show=False),
               itemstyle_opts=opts.ItemStyleOpts(color="#3B4856",color0="#A73835"),
               )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(type_="category",is_scale=True,grid_index=1,boundary_gap=False,
                                 axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                                 axistick_opts=opts.AxisTickOpts(is_show=False),
                                 splitline_opts=opts.SplitLineOpts(is_show=False),
                                 axislabel_opts=opts.LabelOpts(is_show=False),
                                 split_number=20,),
        yaxis_opts=opts.AxisOpts(grid_index=1,is_scale=True,split_number=2,
                                 axislabel_opts=opts.LabelOpts(is_show=False),
                                 axisline_opts=opts.AxisLineOpts(is_show=False),
                                 axistick_opts=opts.AxisTickOpts(is_show=False),
                                 ),

        legend_opts=opts.LegendOpts(is_show=False),

    )
)

#將 Kline, line, bar 圖重疊
overlap_kline_line=kline.overlap(line)

grid_chart=(
    Grid()
    .add(overlap_kline_line,
         grid_opts=opts.GridOpts(pos_left="10%",pos_right="8%",height="50%"),
         )
    .add(bar,
         grid_opts=opts.GridOpts(pos_left="10%",pos_right="8%",pos_top="70%",height="16%"),)
)

grid_chart.render()
