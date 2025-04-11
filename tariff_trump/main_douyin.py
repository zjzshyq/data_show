# https://data.worldbank.org/indicator/SP.POP.TOTL

from sjvisualizer import Canvas,DataHandler,BarRace
import pandas as pd
import warnings
import json

warnings.filterwarnings('ignore')
logo_dir = '../common/logo.png'
with open('../common/colors_cn.json') as f:
    colors = json.load(f)

FPS = 60
DURATION = 0.5
frames = int(FPS*DURATION*60)
excel_dir = 'data/Ukraine_Loan_Repayable_Cumulative_USD.xlsx'
df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df
df.index = df.index + pd.DateOffset(months=1)

for col in df.columns:
    if col != 'Month':  # 排除 Month 列
        df[col] = df[col] / 100  # 将金额转换为亿单位

continent = 'Europe'
countries = pd.read_csv("../common/countries.csv")
asian_countries = countries[countries["continent_en"] == continent]["chinese_name"]
df = df[df.columns.intersection(asian_countries)]
df = df.drop(columns='欧盟', errors="ignore")
df = df.loc[(df != 0).any(axis=1)]

canvas_size_ratio = 0.4
canvas_width = 900 * canvas_size_ratio
canvas_height = 1600 * canvas_size_ratio

canvas = Canvas.canvas()
bar_chart = BarRace.bar_race(df = df, canvas=canvas.canvas,
                             colors=colors, unit='亿',
                             number_of_bars = 10, font_scale = 0.9,
                             width=canvas_width, height=canvas_height+20, x_pos =550, y_pos= 145)
canvas.add_sub_plot(bar_chart)

# title：乌克兰欠谁最多？欧洲各国对乌放贷金额排名（2022-2025）
# cover：援助 or 负债？乌克兰欧洲债主国家排名

'''
数据来源: 德国基尔世界研究所
背景音乐: You Will Come Like Lightning
本排名仅为欧洲对乌克兰援助的贷款金额，全金额或全球排名详见本账号的其他视频
'''

canvas.add_title('欧洲各国对乌克兰贷款金额排名', color=(0,0,0), size_ratio=40)
canvas.add_sub_title('单位: 亿美元(亿)', color=(111,111,111), size_ratio=60, pos_ratio=(2,7.7))
canvas.add_logo(logo_dir, pos_ratio=(0.64, 0.027), size_ratio=22)
canvas.add_time(df=df,time_indicator='month', color=(122, 122, 122),
                pos_ratio=(0.55, 0.82),size_ratio=12)

canvas.play(fps=FPS)