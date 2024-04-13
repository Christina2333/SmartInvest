import pandas as pd
from datetime import datetime
from my.dao.kline_dao import get_by_stock_and_dt_section

stock_list = ['SH600036', 'SH601988', 'SH601006', 'SH600028', 'SH600019', 'SH600900', 'SH600016', 'SZ000002',
              'SH600050', 'SH600519']
stock_name = ['招商银行', '中国银行', '大秦铁路', '中国石化', '宝钢股份', '长江电力', '民生银行', '深万科A', '中国联通',
              '贵州茅台']
stock_percent = [9.0627, 5.6025, 5.4295, 5.1959, 5.1884, 5.0562, 5.0302, 4.8303, 3.5077, 3.0063]

start_time = 20140411
end_time = 20240412

res = []
origin = []
for i in range(0, len(stock_list)):
    stock_code = stock_list[i]
    name = stock_name[i]
    percent = stock_percent[i] / 100
    stock = get_by_stock_and_dt_section(stock_code, start_time, end_time)
    info_origin = [[name, x.stock_code, float(x.close), datetime.strptime(str(x.dt), '%Y%m%d')] for x in stock]
    info = [[name, x.stock_code, float(x.close) * percent, datetime.strptime(str(x.dt), '%Y%m%d')] for x in stock]
    res.extend(info)
    origin.extend(info_origin)

origin_df = pd.DataFrame(origin, columns=['stock_name', 'stock_code', 'close', 'dt'])
origin_df.to_csv('a50_origin.csv', index=False)

df = pd.DataFrame(res, columns=['stock_name', 'stock_code', 'close', 'dt'])
df.sort_values(by='dt', inplace=False)
daily_close_sum = df.groupby('dt')['close'].sum()
daily_close_sum = daily_close_sum.reset_index()
daily_close_sum.columns = ['dt', 'close']
daily_close_sum.to_csv('a50.csv', index=False)
