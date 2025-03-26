import pandas as pd
import re

# 读取 Excel 文件
file_path = "../original_data/Ukraine_Support_Tracker_Release_21.xlsx"
df = pd.read_excel(file_path, sheet_name="Bilateral Assistance, MAIN DATA")

# 确保日期列格式正确
df['announcement_date'] = pd.to_datetime(df['announcement_date'], errors='coerce')

# 提取年月
df['year_month'] = df['announcement_date'].dt.to_period('M')

# 选择需要的列，并将金额转换为数值
df['amount'] = pd.to_numeric(df['tot_sub_activity_value_EUR_OLD'], errors='coerce')

# 过滤掉 earmarked_year >= 2025 的数据
def filter_year(year):
    if isinstance(year, str) and re.match(r'^\d{4}$', year):
        return int(year) < 2025
    elif isinstance(year, str) and re.match(r'^\d{4}-\d{4}$', year):
        return True
    return True

df = df[df['earmarked_year'].apply(filter_year)]

# 仅保留军事援助相关的数据
def is_military_aid(aid_type):
    return isinstance(aid_type, str) and ('military' in aid_type.lower() or 'defense' in aid_type.lower())

df = df[df['aid_type_general'].apply(is_military_aid)]

# 按年月和国家聚合军事援助金额
grouped = df.groupby(['year_month', 'donor'])['amount'].sum().unstack(fill_value=0)

# 计算累积总额
cumulative_df = grouped.cumsum()

# 重置索引并转换年月格式
cumulative_df.index = cumulative_df.index.astype(str)
cumulative_df.reset_index(inplace=True)
cumulative_df.rename(columns={'year_month': 'Month'}, inplace=True)

# 将 Month 列转换为 datetime 类型
cumulative_df['Month'] = pd.to_datetime(cumulative_df['Month'], format='%Y-%m')

# 统一国家名称
columns_rename = {'EU (Commission and Council)': 'EU', 'United Kingdom': 'UK', 'United States': 'USA'}
cumulative_df.rename(columns=columns_rename, inplace=True)

# 删除不需要的列
columns_to_drop = ['FInland', 'European Peace Facility', 'European Investment Bank']
cumulative_df.drop(columns=columns_to_drop, errors='ignore', inplace=True)

# 金额转换为百万单位
unit = 1000000
for col in cumulative_df.columns:
    if col != 'Month':
        cumulative_df[col] = cumulative_df[col] / unit

# 将欧元金额转换为美元（1欧元 = 1.09美元）
for col in cumulative_df.columns:
    if col != 'Month':
        cumulative_df[col] = cumulative_df[col] * 1.09

# 保存处理后的数据到 Excel
output_path = "data/Ukraine_Support_Cumulative_USD.xlsx"
cumulative_df.to_excel(output_path, index=False)

# 输出结果
print(f"Processed military aid data saved to {output_path}")
