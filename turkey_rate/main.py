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
excel_dir = 'data/philippines_gdp_sectors.xlsx'

df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df

df = df.drop(columns=['GDP'])
df = df.round(2)


events = {
    "Marcos\nRule Ends": ["25/02/1986", "25/02/1986"],
    "Joined\nWTO": ["01/01/1995", "01/01/1995"],
    "Labor Export\nExpanded": ["04/04/2000", "04/04/2000"],
    'Duterte\nTook Office':['30/06/2016','30/06/2016']
}
canvas = Canvas.canvas()
lines = LineChart.line_chart(df = df, canvas=canvas.canvas,
                             unit='%', draw_points=False, colors=colors,
                             events=events, draw_all_events=True, time_indicator='year',
                             x_pos=280,height=500,y_pos=240, font_size=22)
canvas.add_sub_plot(lines)

# title：Philippines' Economic Evolution: Industry, Agriculture & Services (1975-2023)
'''
Data Source: WorldBank
BGM: Brand X Music - Extinction
'''
canvas.add_title('Philippines\' GDP Share Trends\nin Industry, Agriculture & Services', color=(0,0,0))
canvas.add_logo(logo_dir, pos_ratio=(0.25, 0.022))
canvas.add_time(df=df,time_indicator='month', color=(121, 121, 121),
                pos_ratio=(0.65, 0.7))

canvas.play(fps=FPS)

