import pandas as pd
from datetime import datetime


def get_read_amt_df():
    df = pd.read_excel('data/各渠道文章每日阅读次数.xls')
    int_columns = ['阅读次数']
    df[int_columns] = df[int_columns].astype(int)
    float_columns = ['阅读次数占比']
    df[float_columns] = df[float_columns].astype(float)
    df['发表日期'] = pd.to_datetime(df['发表日期'], format='%Y%m%d%H')
    df = df[df['传播渠道'] != '全部'].sort_values(by=['内容标题', '发表日期'])
    return df


if __name__ == '__main__':
    df = get_read_amt_df()
    pd.set_option('display.max_rows', None)  # 不限制显示的最大行数
    pd.set_option('display.max_columns', None)  # 不限制显示的最大列数
    pd.set_option('display.width', None)  # 自动调整列宽以适应内容，不限制最大宽度
    print(df)
