import numpy as np
import matplotlib.pyplot as plt

from my.BaseUtils import cal_annual_compound_return, get_drawdown
from my.DataProcess import get_hist_data_from_ywcq

start_date = '2014-05-07'
# start_date = None
end_date = '2024-05-07'
# end_date = None
df = get_hist_data_from_ywcq('../data/oil/162411历史数据.csv', ['收盘'], start_date, end_date, replace={'收盘':'Close'})

plt.figure()
plt.plot(df.index, df['Close'])
plt.title("162411 ETF")
plt.xlabel("Day")
plt.ylabel('Price')
plt.show()

print(f"原油年复合增长率{cal_annual_compound_return(df.iloc[1]['Close'], df.iloc[-1]['Close'], 10):.2%}")
print(f"原油最大回撤为{np.nanmin(get_drawdown(df['Close'])):.4%}")
