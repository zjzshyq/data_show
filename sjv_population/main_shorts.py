# https://data.worldbank.org/indicator/SP.POP.TOTL

from sjvisualizer import Canvas,DataHandler,BarRace
import warnings
import json

warnings.filterwarnings('ignore')
logo_dir = '../common/logo.png'
with open('../common/colors.json') as f:
    colors = json.load(f)

FPS = 60
DURATION = 0.5
frames = int(FPS*DURATION*60)
excel_dir = 'data/population_predictions_2024_2050.xlsx'
df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df

canvas_size_ratio = 0.4
canvas_width = 900 * canvas_size_ratio
canvas_height = 1600 * canvas_size_ratio

canvas = Canvas.canvas()
bar_chart = BarRace.bar_race(df = df, canvas=canvas.canvas,
                             colors=colors, unit='M',
                             number_of_bars = 10, font_scale = 0.9,
                             width=canvas_width, height=canvas_height+20, x_pos =550, y_pos= 145)
canvas.add_sub_plot(bar_chart)

# 标题：【视觉数据】中国人口下滑后的世界人口格局｜1975-2050世界人口变迁
# 封面：中国人口下滑，世界格局将如何改变？
# 数据来源: https://data.worldbank.org/
# 预测模型: ARIMA
# BGM: Nijamena

canvas.add_title('Global Population Race (1975-2050)', color=(0,0,0), size_ratio=40)
canvas.add_sub_title('Unit: Million (M)', color=(111,111,111), size_ratio=60, pos_ratio=(2,7.5))
# canvas.add_logo(logo_dir, pos_ratio=(0.67, 0.03), size_ratio=(20,20))
canvas.add_time(df=df,time_indicator='year', color=(122, 122, 122), pos_ratio=(0.54, 0.786))

canvas.play(fps=FPS)