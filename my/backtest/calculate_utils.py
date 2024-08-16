from datetime import datetime

import numpy as np
import pandas as pd


def calculate_slope(df, y_name, window_size=7):
    """
    计算 df 中 y_name 这个字段的斜率
    """
    name = y_name + '_slope'
    df[name] = np.nan  # 初始化一个全为 NaN 的列
    for i in range(window_size, len(df)):
        df.at[df.index[i], name] = calculate_slope_at_point(df, i, y_name, window_size)


def date_to_sec(date):
    """
    datetime.date转为 s
    """
    my_datetime = datetime.combine(date, datetime.min.time())
    return my_datetime.timestamp()


def calculate_slope_at_point(df, point_index, y_name, window_size=5):
    if window_size % 2 == 0:
        window_size += 1

    half_window = window_size // 2

    start_index = max(0, point_index - half_window)
    end_index = min(len(df), point_index + half_window + 1)

    # 转为时间戳
    # x_values = df.index[start_index:end_index].apply(date_to_sec)
    x_values = pd.Series(pd.to_datetime(df.index[start_index:end_index]).astype(np.int64) // 10**9)
    y_values = df[y_name].iloc[start_index:end_index]

    if y_values.isna().any():
        slope = np.nan
    else:
        slope, _ = np.polyfit(x_values, y_values, 1)
    return slope
