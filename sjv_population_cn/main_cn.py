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
excel_dir = '/Users/huyiqing/PycharmProjects/data_show/sjv_population_v2/data/population_predictions_2024_2050_cn.xlsx'
df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df

canvas = Canvas.canvas()
bar_chart = BarRace.bar_race(df = df, canvas=canvas.canvas,
                             colors=colors, unit='M',
                             number_of_bars = 12, font_scale = 0.95,
                             x_pos=170)
canvas.add_sub_plot(bar_chart)

# 标题：【预测】中国人口下滑背后的世界人口格局｜1975-2050世界人口变迁
# 封面：中国人口下滑，世界格局将如何改变？
# 数据来源: https://data.worldbank.org/
# 预测模型: ARIMA
# BGM: Nijamena
# 需要具体数据的小伙伴，可以在评论区留言哦

canvas.add_title('全球人口增长变化及预测 (1975-2050)', color=(0,0,0))
canvas.add_sub_title('单位: 百万 (M)', color=(111,111,111))
canvas.add_logo(logo_dir, pos_ratio=(0.77, 0))
canvas.add_time(df=df,time_indicator='year', color=(122, 122, 122), pos_ratio=(0.65, 0.7))

canvas.play(fps=FPS)