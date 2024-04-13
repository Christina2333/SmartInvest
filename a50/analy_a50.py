import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from my.BaseUtils import cal_annual_compound_return
from my.BaseUtils import get_drawdown

a50 = pd.read_csv('a50.csv')
print(
    f"a50, 年化收益为{cal_annual_compound_return(a50['close'].iloc[0], a50['close'].iloc[-1], 10):.4%}, "
    f"最大回撤为{np.nanmin(get_drawdown(a50['close'])):.4%}")

plt.figure(1)
plt.plot(a50['dt'], a50['close'])
plt.xticks(np.arange(0, len(a50['dt']), 500))
plt.title("mock a50 top 10")
plt.xlabel("Day")
plt.ylabel('Price')
plt.legend()
plt.show()

stock_list = ['SH600036', 'SH601988', 'SH601006', 'SH600028', 'SH600019', 'SH600900', 'SH600016', 'SZ000002',
              'SH600050', 'SH600519']
a50_origin = pd.read_csv('a50_origin.csv')

for code in stock_list:
    plt.figure()
    df = a50_origin[a50_origin['stock_code'] == code]
    print(f"股票{code}, 年化收益为{cal_annual_compound_return(df['close'].iloc[0], df['close'].iloc[-1], 10):.4%}, "
          f"最大回撤为{np.nanmin(get_drawdown(df['close'])):.4%}")
    df.sort_values(by='dt')
    plt.plot(df.dt, df.close, label=code)
    plt.xticks(np.arange(0, len(df.dt), 500))
    plt.legend()
    plt.show()

print()
