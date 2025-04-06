import pandas as pd
import re

# 读取数据
file_path = "../original_data/Ukraine_Support_Tracker_Release_21.xlsx"
df = pd.read_excel(file_path, sheet_name="Bilateral Assistance, MAIN DATA")

# 转换日期格式
df['announcement_date'] = pd.to_datetime(df['announcement_date'], errors='coerce')

# 提取年月
df['year_month'] = df['announcement_date'].dt.to_period('M')

# 转换金额字段为数字
df['amount'] = pd.to_numeric(df['tot_sub_activity_value_EUR_OLD'], errors='coerce')

# 过滤掉 earmarked_year >= 2025 的数据
def filter_year(year):
    if isinstance(year, str) and re.match(r'^\d{4}$', year):
        return int(year) < 2025
    elif isinstance(year, str) and re.match(r'^\d{4}-\d{4}$', year):
        return True
    return True

df = df[df['earmarked_year'].apply(filter_year)]

# 识别贷款和捐赠
# 贷款条件：loan_mat == 1 或 loan_int == 1 或 loan_gra == 1
df['is_loan'] = (df['loan_mat'] == 1) | (df['loan_int'] == 1) | (df['loan_gra'] == 1)

# 纯捐赠条件：is_loan == False
df['is_grant'] = ~df['is_loan']

# 分别筛选贷款和纯捐赠数据
loan_df = df[df['is_loan']].copy()
grant_df = df[df['is_grant']].copy()

# 聚合为各月各国总额
def prepare_cumulative_table(df):
    grouped = df.groupby(['year_month', 'donor'])['amount'].sum().unstack(fill_value=0)
    cumulative = grouped.cumsum()
    cumulative.index = cumulative.index.astype(str)
    cumulative.reset_index(inplace=True)
    cumulative.rename(columns={'year_month': 'Month'}, inplace=True)
    cumulative['Month'] = pd.to_datetime(cumulative['Month'], format='%Y-%m')

    # 重命名列
    rename_map = {'EU (Commission and Council)': 'EU', 'United Kingdom': 'UK', 'United States': 'USA'}
    cumulative.rename(columns=rename_map, inplace=True)

    # 删除不需要的列
    columns_to_drop = ['FInland', 'European Peace Facility', 'European Investment Bank']
    cumulative.drop(columns=columns_to_drop, errors='ignore', inplace=True)

    # 转换单位为百万
    for col in cumulative.columns:
        if col != 'Month':
            cumulative[col] = cumulative[col] / 1_000_000

    # 欧元转美元，汇率 1 EUR = 1.09 USD
    for col in cumulative.columns:
        if col != 'Month':
            cumulative[col] = cumulative[col] * 1.09

    return cumulative

# 生成结果
loan_cumulative = prepare_cumulative_table(loan_df)
grant_cumulative = prepare_cumulative_table(grant_df)

# 保存到 Excel
loan_output_path = "data/Ukraine_Loan_Cumulative_USD.xlsx"
grant_output_path = "data/Ukraine_Grant_Cumulative_USD.xlsx"

loan_cumulative.to_excel(loan_output_path, index=False)
grant_cumulative.to_excel(grant_output_path, index=False)

print(f"Loan data saved to {loan_output_path}")
print(f"Grant data saved to {grant_output_path}")
