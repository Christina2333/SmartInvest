import pandas as pd

def ma(df, name, window):
    """
    计算普通的滑动平均
    @param df     dataframe
    @param name   dataframe中要计算的字段
    @param window 计算多少根线的平均
    @return
    """
    return df[name].rolling(window=window).mean()



def weighed_sma(df, n, m=1, name = 'Close'):
    """
    计算带权重的移动平均 SMA
    Y=(X * M + Y' * (N - M)) / N
    """
    sma_values = []

    prices = df[name].values

    for i in range(len(prices)):
        if i < n:
            sma_values.append(prices[i])
        else:
            previous_sma = sma_values[-1]
            current_price = prices[i]
            sma_values.append((current_price * m + previous_sma * (n - m)) / n)

    return pd.DataFrame(index=df.index, columns=[name], data=sma_values)