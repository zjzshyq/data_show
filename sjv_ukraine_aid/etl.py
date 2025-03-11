import pandas as pd

# 读取 Excel 文件
file_path = "/Users/huyiqing/PycharmProjects/data_show/original_data/Ukraine_Support_Tracker_Release_21.xlsx"
df = pd.read_excel(file_path, sheet_name="Bilateral Assistance, MAIN DATA")

# 确保日期列格式正确
df['announcement_date'] = pd.to_datetime(df['announcement_date'], errors='coerce')

# 提取年月
df['year_month'] = df['announcement_date'].dt.to_period('M')

# 选择需要的列，并将金额转换为数值
df['amount'] = pd.to_numeric(df['tot_sub_activity_value_EUR_OLD'], errors='coerce')

# 按年月和国家聚合援助金额
grouped = df.groupby(['year_month', 'donor'])['amount'].sum().unstack(fill_value=0)

# 计算累积总额
cumulative_df = grouped.cumsum()

# 重置索引并转换年月格式
cumulative_df.index = cumulative_df.index.astype(str)
cumulative_df.reset_index(inplace=True)
cumulative_df.rename(columns={'year_month': 'Month'}, inplace=True)

# 将 Month 列转换为 datetime 类型
cumulative_df['Month'] = pd.to_datetime(cumulative_df['Month'], format='%Y-%m')

# 将其他列的数据除以 1,000,000
for col in cumulative_df.columns:
    if col != 'Month':  # 排除 Month 列
        cumulative_df[col] = cumulative_df[col] / 1000000

# 保存处理后的数据到 Excel
output_path = "/sjv_ukraine_aid/data/Ukraine_Support_Cumulative.xlsx"
cumulative_df.to_excel(output_path, index=False)

# 输出结果
print(f"Processed data saved to {output_path}")