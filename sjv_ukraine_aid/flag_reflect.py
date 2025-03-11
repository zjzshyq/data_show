import pandas as pd
import os
import cairosvg

# 1. 读取数据并删除 "Arab World" 列
input_file = "/sjv_ukraine_aid/data/Ukraine_Support_Cumulative.xlsx"
df = pd.read_excel(input_file)


# 2. 读取 countries.csv 文件，获取国名和简称的映射
countries_file = "/Users/huyiqing/PycharmProjects/data_show/common/countries.csv"
countries_mapping = pd.read_csv(countries_file)
country_to_code = dict(zip(countries_mapping["full_name"], countries_mapping["short_name"]))

# 3. 查找国旗图片并转换格式
flags_source_dir = "/Users/huyiqing/PycharmProjects/data_show/common/round_flags"
flags_target_dir = "/sjv_ukraine_aid/assets"

# 确保目标目录存在
os.makedirs(flags_target_dir, exist_ok=True)

# 记录未找到或映射不上的国家
missing_countries = []

# 遍历数据中的国家列
for country in df.columns[1:]:  # 第一列是年份，跳过
    # 获取国家简称
    code = country_to_code.get(country)
    if not code:
        missing_countries.append(country)
        continue

    # 构建 SVG 图片路径
    flag_svg = f"{code.lower()}.svg"
    flag_svg_path = os.path.join(flags_source_dir, flag_svg)

    # 构建目标 PNG 图片路径
    flag_png_path = os.path.join(flags_target_dir, f"{country}.png")

    # 检查 SVG 图片是否存在
    if os.path.exists(flag_svg_path):
        try:
            # 将 SVG 转换为 PNG
            cairosvg.svg2png(url=flag_svg_path, write_to=flag_png_path)
            print(f"已转换并复制 {country} 的国旗图片: {country}.png")
        except Exception as e:
            print(f"转换 {country} 的国旗图片失败: {e}")
            missing_countries.append(country)
    else:
        missing_countries.append(country)

# 4. 列出未找到或映射不上的国家
if missing_countries:
    print("以下国家未找到或映射不上：")
    for country in missing_countries:
        print(f"- {country}")
else:
    print("所有国家的国旗图片均已找到并转换。")
