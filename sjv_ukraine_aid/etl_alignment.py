import pandas as pd

# 读取 total_aid 数据并转换为百万美元
total_aid_path = "data/total_aid.txt"
total_aid_df = pd.read_csv(total_aid_path, delimiter='\t')
# row_name = 'Total'
row_name = 'Military'

# 将 total_aid 的金额（十亿欧元）转换为百万美元
unit = 1000  # 转换为百万美元
# unit = 1000000 # 转为k
total_aid_df[row_name] = total_aid_df[row_name] * 1.09 * unit

# 读取 Ukraine_Support_Cumulative_USD.xlsx 数据
file_path = "data/Ukraine_Support_Cumulative_USD.xlsx"
cumulative_df = pd.read_excel(file_path)

# 获取最后一行的累加值
last_row = cumulative_df.iloc[-1, 1:]  # 跳过第一列 'Month'

# 用于比对和替换的数据
not_updated_countries = []

# 遍历 total_aid 中的每个国家
for index, row in total_aid_df.iterrows():
    country = row['Country']
    total_aid_amount = row[row_name]

    if country in cumulative_df.columns:  # 如果国家在累积数据中
        # 获取该国家的最后一个值
        last_value = last_row[country]

        # 计算比值
        ratio = total_aid_amount / last_value

        # 替换数据
        cumulative_df[country] = cumulative_df[country] * ratio
    else:
        # 如果国家不在数据中，记录
        not_updated_countries.append(country)

# 保存处理后的数据到新的 Excel 文件
output_path = "data/Updated_Ukraine_Support_Cumulative_USD.xlsx"
cumulative_df.to_excel(output_path, index=False)

# 打印没有更新数据的国家名称
print("Countries not found in the data for replacement:")
for country in not_updated_countries:
    print(country)

print(f"Processed data saved to {output_path}")
del cumulative_df