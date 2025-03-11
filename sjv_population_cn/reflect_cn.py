import pandas as pd
import os

# 步骤 1: 读取人口预测数据
population_file = "/sjv_population/data/population_predictions_2024_2050.xlsx"
df_population = pd.read_excel(population_file)

# 步骤 2: 读取英文和中文国家名称映射
countries_file = "/common/countries.csv"
df_countries = pd.read_csv(countries_file)

# 创建英文全名到中文名称的映射字典
country_mapping = dict(zip(df_countries['full_name'], df_countries['chinese_name']))

# 步骤 3: 修改列名为中文
new_columns = {}
for col in df_population.columns:
    if col in country_mapping:
        new_columns[col] = country_mapping[col]  # 将英文列名替换为中文
    else:
        new_columns[col] = col  # 如果没有映射，保留原名

# 修改列名
df_population.rename(columns=new_columns, inplace=True)

# 保存修改后的数据
output_population_file = "/sjv_population/data/population_predictions_2024_2050_cn.xlsx"
df_population.to_excel(output_population_file, index=False)

print(f"Data with Chinese country names saved to {output_population_file}")

# 步骤 4: 修改图片文件名
assets_dir = "/sjv_population_cn/assets"
for filename in os.listdir(assets_dir):
    if filename.endswith('.png'):
        country_name = filename.split('.')[0]  # 获取文件名（不包括扩展名）
        if country_name in country_mapping:
            new_filename = country_mapping[country_name] + ".png"  # 新的文件名
            os.rename(os.path.join(assets_dir, filename), os.path.join(assets_dir, new_filename))

print("Image file names have been updated.")
