import pandas as pd
import os

# 读取 Excel 文件
file_path = '../original_data/土叙汇率变化.xlsx'  # 替换为你的文件路径
df = pd.read_excel(file_path)

# 提取所有的列名，并找到从1995年1月到2025年3月的列
columns = df.columns.tolist()

# 创建包含每个月份数据的列名列表，排除季度数据
time_columns = [col for col in columns if 'Q' not in col and 'Series' not in col and 'Country' not in col]

# 选取土耳其的数据
df_turkey = df[df['Country'] == 'Turkey'][['Country', 'Country Code', 'Series', 'Series Code'] + time_columns]

# 通过 melt 操作将数据转换为长格式
df_long = df_turkey.melt(id_vars=['Country', 'Country Code', 'Series', 'Series Code'],
                         value_vars=time_columns,
                         var_name='Month',
                         value_name='Turkey')

# 使用 split 和 replace 处理日期格式
df_long['Month'] = df_long['Month'].str.split(' ').str[0].str.replace('M', '-', regex=False)
df_long = df_long[~df_long['Month'].str.contains('^\d{4}$')]
print(df_long.head(10))
# 转换为 datetime 类型
df_long['Month'] = pd.to_datetime(df_long['Month'], errors='coerce') #.dt.to_period('M')

# 过滤掉 1995年1月之前的数据
df_long = df_long[df_long['Month'] >= '1995-01-01']

# 去除无效的数据行（如时间列为 NaT 或土耳其数据为空）
df_long = df_long.dropna(subset=['Month', 'Turkey'])

# 按照 Month 排序
df_long = df_long.sort_values(by='Month', ascending=True)

# 只保留 Month 和 Turkey 列
df_long = df_long[['Month', 'Turkey']]
# df_long['Turkey'] = 1 / df_long['Turkey']

# 输出结果到新的 Excel 文件
output_file_path = 'data/processed_turkey_exchange_rate_from_1995.xlsx'
if os.path.exists(output_file_path):
    os.chmod(output_file_path, 0o777)
    os.remove(output_file_path)
df_long.to_excel(output_file_path, index=False)
print(df_long.head(5))
del df_long
