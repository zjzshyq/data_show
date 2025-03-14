import requests
import pandas as pd
from datetime import datetime

# 定义指标代码
indicators = {
    "Agriculture": "NV.AGR.TOTL.ZS",
    "Industry": "NV.IND.TOTL.ZS",
    "Services": "NV.SRV.TOTL.ZS",
    "GDP": "NY.GDP.MKTP.CD"  # 添加GDP指标
}

# 定义API URL
base_url = "https://api.worldbank.org/v2/country/PH/indicator/{indicator}?format=json&date=1950:2024"

# 存储数据
data = {}

# 获取数据
for sector, code in indicators.items():
    url = base_url.format(indicator=code)
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()[1]  # 获取实际数据部分
        for entry in json_data:
            year = entry["date"]
            value = entry["value"]
            if year not in data:
                data[year] = {"Year": year}
            data[year][sector] = value

# 将数据转换为DataFrame
df = pd.DataFrame.from_dict(data, orient="index")

# 将Year列转换为datetime类型
df["Year"] = pd.to_datetime(df["Year"], format="%Y")

# 将Year列设置为索引
df.set_index("Year", inplace=True)
# 将GDP单位从美元转换为十亿美元
if "GDP" in df.columns:
    df["GDP"] = df["GDP"] / 1_000_000_000  # 转换为十亿美元

df.index = df.index.year
df = df.sort_index(ascending=True)
# 保存为Excel文件
output_file = "data/philippines_gdp_sectors.xlsx"
df.to_excel(output_file)
del df

print(f"Excel文件已生成：{output_file}")
