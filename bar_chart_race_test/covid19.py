import bar_chart_race as bcr
import pandas as pd
import matplotlib.pyplot as plt

video_path = "/Users/huyiqing/Movies/py4v/race.mp4"
countries_df = pd.read_csv('../common/countries.csv')

# 载入 bar_chart_race 数据集
df = bcr.load_dataset('covid19')
country_list = df.columns  # 获取数据集中的国家名称

# 过滤出匹配的国家信息
matched_countries = countries_df[countries_df['full_name'].isin(country_list)]

# **步骤 1：修改 df 列名（英文 → 中文）**
country_name_map = dict(zip(matched_countries['full_name'], matched_countries['chinese_name']))
df.rename(columns=country_name_map, inplace=True)

bcr.bar_chart_race(df,
                   filename=video_path,
                   orientation='h',
                   title='各国COIVD19感染人数',
                   #img_label_folder='/Users/huyiqing/Movies/assets/nation_flags_chinese',
                   #tick_image_mode='fixed'
                   )
print(f"视频已保存到: {video_path}")