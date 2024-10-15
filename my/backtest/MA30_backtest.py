"""
针对 QQQ 数据回测，
当跌破 MA30时卖出，高于 MA30，且成交量大于均值时买入，其余时间空仓
"""
from datetime import datetime

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from my.BaseUtils import cal_period_perf_indicator, cal_annual_compound_return
from my.DataProcess import get_hist_data_from_ywcq
from my.utils.index_utils import ma


start_date = '2004-09-13'
end_date = '2024-09-13'

qqq = get_hist_data_from_ywcq('../data/usa/QQQ历史数据_wk.csv',
                              index_ids=['收盘', '交易量'],
                              start_date=start_date, end_date=end_date,
                              replace={"收盘": "Close", "交易量": "Vol"}
                              )

close = pd.DataFrame(data=qqq['Close'], index=qqq.index, columns=['Close'])

# 每天的涨跌幅度
asset_ret = close.pct_change()
# 指数每天的收益
res = (1 + asset_ret).cumprod()

# 计算 MA30移动平均
qqq['MA30'] = ma(qqq, 'Close', 30)
qqq['MVOL'] = ma(qqq, 'Vol', 4)

# 仓位
# qqq['target_wgt'] = 0
hold_wgt = pd.DataFrame(data=0, index=qqq.index, columns=['Close'])

prev_idx = None
last_wgt = 1

for idx, value in qqq.iterrows():
    # 上一次持仓
    if prev_idx is not None:
        last_wgt = hold_wgt.loc[prev_idx]['Close']
    if not np.isnan(value['MA30']):
        if value['Close'] > value['MA30']:
            # 如果要加仓，需要判断交易量是否满足条件
            if last_wgt == 0:
                if value['Vol'] > value['MVOL']:
                    hold_wgt.at[idx, 'Close'] = 1
                    # qqq.at[idx, 'target_wgt'] = 1
            else:
                # qqq.at[idx, 'target_wgt'] = 1
                hold_wgt.at[idx, 'Close'] = 1
    prev_idx = idx

res['account'] = (1 + (hold_wgt.shift(1) * asset_ret).sum(axis=1)).cumprod()

fig, axs = plt.subplots(3, 1)
# 收盘价和 ma
axs[0].plot(qqq.index, qqq['Close'], color="red", linewidth=1, label='Close')
axs[0].plot(qqq.index, qqq['MA30'], color='blue', label='MA30')
axs[0].set_xlabel('time')
axs[0].set_ylabel('Price')
axs[0].set_title('QQQ ETF')
axs[0].legend()

# 成交量
axs[1].bar(qqq.index, qqq['Vol'], color='blue', linewidth=1, label="Vol")
axs[1].plot(qqq.index, qqq['MVOL'], color='red', linewidth=1, label="MAVOL")
axs[1].set_xlabel('time')
axs[1].set_ylabel('Vol')
axs[1].set_title('Vol')
axs[1].legend()


axs[2].plot(qqq.index, hold_wgt, color='red', linewidth=1, label="target_wgt")
axs[2].set_xlabel('time')
axs[2].set_ylabel('wgt')
axs[2].set_title('target_wgt')
axs[2].legend()

plt.tight_layout()
plt.show()

res.loc[:, ['Close', 'account']].plot(figsize=(16, 8), grid=True)
result = cal_period_perf_indicator(res.loc[:, ['Close', 'account']])
print(result)

# 计算年化收益率
year_interval = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days / 365.0

qqq_return = cal_annual_compound_return(res['Close'].iloc[1], res['Close'].iloc[-1], year_interval)
invest_return = cal_annual_compound_return(res['account'].iloc[1], res['account'].iloc[-1], year_interval)
print(f"近{year_interval:.2f}年，指数 QQQ 年化收益率为{qqq_return:.4%}, 投资策略年化收益率为{invest_return:.4%}")