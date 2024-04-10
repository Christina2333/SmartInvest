import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from my.BaseUtils import cal_annual_compound_return, get_drawdown

df = pd.read_csv('../data/commodity/518880.SS.csv').set_index('Date')

plt.figure()
plt.plot(df.index, df['Close'])
plt.title(f"gold price")
plt.xlabel("Day")
plt.ylabel('Price')
plt.show()


print(f"黄金年复合增长率{cal_annual_compound_return(df.iloc[1]['Close'], df.iloc[-1]['Close'], 10.75):.2%}")
print(f"黄金最大回撤为{np.nanmin(get_drawdown(df['Close'])):.4%}")
