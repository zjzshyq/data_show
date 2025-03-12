# 数据来源：https://www.ifw-kiel.de/kiel-institute-data-hub/
# https://www.ifw-kiel.de/topics/war-against-ukraine/ukraine-support-tracker/
# https://www.ifw-kiel.de/publications/ukraine-support-tracker-data-20758/

from sjvisualizer import Canvas,DataHandler,BarRace,LineChart
import warnings
import json
warnings.filterwarnings('ignore')

logo_dir = '/Users/huyiqing/PycharmProjects/data_show/common/logo.png'
with open('/Users/huyiqing/PycharmProjects/data_show/common/colors.json') as f:
    colors = json.load(f)

FPS = 60
DURATION = 0.5
frames = int(FPS*DURATION*120)
excel_dir = '/Users/huyiqing/PycharmProjects/data_show/sjv_ukraine_aid/data/Ukraine_Support_Cumulative.xlsx'
df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df

canvas = Canvas.canvas()
bar_chart = BarRace.bar_race(df = df, canvas=canvas.canvas,
                             colors=colors, unit='M',
                             number_of_bars = 15, font_scale = 0.95,
                             x_pos=170)
canvas.add_sub_plot(bar_chart)

canvas.add_title('Ukraine Aid 202201-202412', color=(0,0,0))
canvas.add_sub_title('Unit: Million (M)', color=(111,111,111))
canvas.add_logo(logo_dir, pos_ratio=(0.77, 0))
canvas.add_time(df=df,time_indicator='month', color=(121, 121, 121), pos_ratio=(0.65, 0.7))

canvas.play(fps=FPS)
