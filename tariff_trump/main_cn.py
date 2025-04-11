# https://www.cbsnews.com/news/trump-reciprocal-tariffs-liberation-day-list/

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
frames = int(FPS*DURATION*120)
excel_dir = 'data/tariff_trump_sub.xlsx'
df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df
df.index = df.index + pd.DateOffset(months=1)

canvas = Canvas.canvas()
bar_chart = BarRace.bar_race(df = df, canvas=canvas.canvas,
                             colors=colors, unit='%', time_indicator='year',
                             number_of_bars = 10, font_scale = 0.95,
                             x_pos=170, height=620, ratio_crt=0.5)
canvas.add_sub_plot(bar_chart)

# title:
# cover：
'''
Updated: 9 April 2025
Data Source: White House
Music: You Will Come Like Lightning
'''

canvas.add_title('', color=(0,0,0))
canvas.add_logo(logo_dir, pos_ratio=(0.78, 0))

canvas.play(fps=FPS)
