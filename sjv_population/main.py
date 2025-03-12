# https://data.worldbank.org/indicator/SP.POP.TOTL
from sjvisualizer import Canvas,DataHandler,BarRace,LineChart
import warnings
import json
warnings.filterwarnings('ignore')

with open('/Users/huyiqing/PycharmProjects/data_show/common/colors.json') as f:
    colors = json.load(f)

FPS = 60
DURATION = 0.5
frames = int(FPS*DURATION*60)
excel_dir = '/Users/huyiqing/PycharmProjects/data_show/sjv_population/data/population_predictions_2024_2050.xlsx'
df = DataHandler.DataHandler(excel_file=excel_dir, number_of_frames=frames).df

# 主画布
# 数据来源
canvas = Canvas.canvas()
bar_chart = BarRace.bar_race(df = df, canvas=canvas.canvas,
                             colors=colors, unit='M', number_of_bars = 12, font_scale = 0.95)
canvas.add_sub_plot(bar_chart)

# line chart
# df_china_india = df[['China','India']]
# df_china_india['China'] = df_china_india['China']/1000
# df_china_india['India'] = df_china_india['India']/1000
#
# chart_width = canvas.width / 4
# chart_height = canvas.height / 4
# x_pos = (canvas.width - chart_width) * 0.75
# y_pos = (canvas.height - chart_height) * 0.75
# line_width = int(1 + chart_height/100)
# line_chart = LineChart.line_chart(df =df_china_india, canvas=canvas.canvas, colors=colors,
#                                   width=chart_width, height=chart_height, x_pos=x_pos, y_pos=y_pos,
#                                   draw_points=False, unit='B', line_width= line_width, font_size= 20)
# canvas.add_sub_plot(line_chart)
'''
India vs The World: Population Change (1975-2050) | Dynamic Data Visualization
Data source: worldbank.org
Prediction model: ARIMA
BGM: Timberman--Nijamena
If you need the data in the video, please leave the comment below.
'''
canvas.add_title('Global Population Race (1975-2050)', color=(0,0,0))
canvas.add_sub_title('Unit: Million (M)', color=(111,111,111))
canvas.add_logo('../common/logo.png', pos_ratio=(0.77, 0))
canvas.add_time(df=df,time_indicator='year', color=(176, 23, 31), pos_ratio=(0.7, 0.7))

canvas.play(fps=FPS)
