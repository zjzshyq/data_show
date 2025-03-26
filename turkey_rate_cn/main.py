# 世界银行
from sjvisualizer import Canvas,DataHandler,LineChart
import warnings
import json
warnings.filterwarnings('ignore')

with open('../common/colors.json') as f:
    colors = json.load(f)

logo_dir = '../common/logo.png'
FPS = 60
DURATION = 0.5
frames = int(FPS*DURATION*120)
excel_dir = 'data/processed_turkey_exchange_rate_from_1995.xlsx'

df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df

events = {
    "Erdogan\nTook Office": ["28/08/2014", "28/08/2014"],
    "Coup\nAttempt": ["15/07/2016", "15/07/2016"],
    "Lira\nCrisis": ["01/01/2018", "31/12/2018"],
    "Erdogan\nEconomic\nPolicy": ["01/01/2021", "24/03/2025"]
}
canvas = Canvas.canvas()
lines = LineChart.line_chart(df = df, canvas=canvas.canvas,
                             unit='', draw_points=False, colors=colors,
                             events=events, draw_all_events=True, time_indicator='month',
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

