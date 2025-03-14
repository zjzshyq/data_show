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


events = {
    "老马科斯\n独裁结束": ["25/02/1986", "25/02/1986"],
    "加入\nWTO": ["01/01/1995", "01/01/1995"],
    "大规模\n劳务派遣": ["04/04/2000", "04/04/2000"],
    '杜特尔特\n上任':['30/06/2016','30/06/2016']
}
canvas = Canvas.canvas()
lines = LineChart.line_chart(df = df, canvas=canvas.canvas,
                             unit='%', draw_points=False, colors=colors,
                             events=events, draw_all_events=True, time_indicator='year',
                             x_pos=280,height=500,y_pos=240, font_size=25)
canvas.add_sub_plot(lines)

# title：杜特尔特被捕背后的菲律宾三大产业的变革(1975-2024)
# cover：菲律宾政治乱象背后的三大产业畸
'''
数据来源: WorldBank
BGM: Extinction
'''
canvas.add_title('菲律宾三大产业占GDP比重变化', color=(0,0,0))
canvas.add_logo(logo_dir, pos_ratio=(0.27, 0))
canvas.add_time(df=df,time_indicator='month', color=(121, 121, 121),
                pos_ratio=(0.65, 0.7))

canvas.play(fps=FPS)

