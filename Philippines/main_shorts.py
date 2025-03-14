# 世界银行
from sjvisualizer import Canvas,DataHandler,LineChart
import warnings
import json
warnings.filterwarnings('ignore')

with open('data/colors.json') as f:
    colors = json.load(f)
logo_dir = '../common/logo.png'
FPS = 60
DURATION = 0.5
frames = int(FPS*DURATION*120)
excel_dir = 'data/philippines_gdp_sectors_cn.xlsx'

df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df

df = df.drop(columns=['GDP'])
df = df.round(2)

canvas_size_ratio = 0.4
canvas_width = 900 * canvas_size_ratio
canvas_height = 1600 * canvas_size_ratio

canvas = Canvas.canvas()
lines = LineChart.line_chart(df = df, canvas=canvas.canvas,
                             unit='%', draw_points=False, colors=colors,time_indicator='year',
                             width=canvas_width, height=canvas_height+20, x_pos =550, y_pos= 145)
canvas.add_sub_plot(lines)

# title：杜特尔特被捕背后的菲律宾三大产业的变革(1975-2023)
'''
数据来源: WorldBank
BGM: Extinction
'''
canvas.add_title('菲律宾政治乱象背后\n三大产业占GDP比重变化', color=(0,0,0), size_ratio=40, pos_ratio=(2,15))
canvas.add_logo(logo_dir, pos_ratio=(0.37, 0), size_ratio=20)
canvas.add_time(df=df,time_indicator='month', color=(122, 122, 122),
                pos_ratio=(0.52, 0.82),size_ratio=12)
canvas.play(fps=FPS)

