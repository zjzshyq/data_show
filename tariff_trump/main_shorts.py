# https://data.worldbank.org/indicator/SP.POP.TOTL

from sjvisualizer import Canvas,DataHandler,BarRace
import pandas as pd
import warnings
import json

warnings.filterwarnings('ignore')
logo_dir = '../common/logo.png'
with open('../common/colors.json') as f:
    colors = json.load(f)

FPS = 60
DURATION = 0.5
frames = int(FPS*DURATION*60)
excel_dir = 'data/Ukraine_Loan_Repayable_Cumulative_USD.xlsx'
df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df
df.index = df.index + pd.DateOffset(months=1)

# 各地区捐赠
continent = 'Europe'
countries = pd.read_csv("../common/countries.csv")
asian_countries = countries[countries["continent_en"] == continent]["full_name"]
df = df[df.columns.intersection(asian_countries)]
df = df.drop(columns='EU', errors="ignore")
df = df.loc[(df != 0).any(axis=1)]

canvas_size_ratio = 0.4
canvas_width = 900 * canvas_size_ratio
canvas_height = 1600 * canvas_size_ratio

canvas = Canvas.canvas()
bar_chart = BarRace.bar_race(df = df, canvas=canvas.canvas,
                             colors=colors, unit='M',
                             number_of_bars = 10, font_scale = 0.9,
                             width=canvas_width, height=canvas_height+20, x_pos =550, y_pos= 145)
canvas.add_sub_plot(bar_chart)

# title:  Who Does Ukraine Owe? Countries Lending Aid (2022-2025)
'''
Data source: ifw-kiel.de
BGM: You Will Come Like Lightning
'''
canvas.add_title('European Loans to Ukraine (2022-2025)', color=(0,0,0), size_ratio=40)
canvas.add_sub_title('Unit: Million USD(M)', color=(111,111,111), size_ratio=60, pos_ratio=(2,7.8))
canvas.add_logo(logo_dir, pos_ratio=(0.68, 0.02), size_ratio=20)
canvas.add_time(df=df,time_indicator='month', color=(122, 122, 122),
                pos_ratio=(0.56, 0.82),size_ratio=12)

canvas.play(fps=FPS)