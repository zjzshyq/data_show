import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from openpyxl import Workbook

# 读取数据
df = pd.read_excel("./data/top_30_countries_population_millions.xlsx")

# 设置年份为索引
df.set_index("Year", inplace=True)

# 定义预测函数
def predict_population(data, years_to_predict):
    # 拟合 ARIMA 模型
    model = ARIMA(data, order=(5, 1, 0))  # ARIMA(p, d, q) 参数可以根据数据调整
    model_fit = model.fit()
    # 预测未来数据
    forecast = model_fit.forecast(steps=years_to_predict)
    return forecast

# 预测 2024-2050 年的人口数据
years_to_predict = 2050 - 2023  # 预测 27 年
predictions = {}

for country in df.columns:
    # 获取历史数据
    historical_data = df[country]
    # 预测未来数据
    forecast = predict_population(historical_data, years_to_predict)
    # 将预测结果保存到字典中
    predictions[country] = forecast

# 创建新的 DataFrame 用于保存预测结果
prediction_years = list(range(2024, 2051))  # 2024-2050 年
prediction_df = pd.DataFrame({"Year": prediction_years})

# 将预测结果添加到 DataFrame 中
for country, forecast in predictions.items():
    prediction_df[country] = forecast.values

# 将历史数据和预测数据合并
full_df = pd.concat([df.reset_index(), prediction_df], ignore_index=True)

# 保存结果到新的 Excel 文件
full_df.to_excel("population_predictions_2024_2050.xlsx", index=False)

print("预测完成，结果已保存为 'population_predictions_2024_2050.xlsx'")