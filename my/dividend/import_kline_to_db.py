import pysnowball as ball
from my.utils.KLineUtils import get_time
from my.dao.kline_dao import KLine
from my.utils.DbUtils import insert

token = '117c88d07cecb77a9963ff144c803750b02ec004'

stock_list = ['SH688303', 'SH601988', 'SH601939', 'SH601919', 'SH601916', 'SH601838', 'SH601818', 'SH601699',
              'SH601658', 'SH601398', 'SH601377', 'SH601328', 'SH601318', 'SH601288', 'SH601229', 'SH601225',
              'SH601169', 'SH601166', 'SH601088', 'SH601009', 'SH601006', 'SH600919', 'SH600741', 'SH600585',
              'SH600438', 'SH600188', 'SH600089', 'SH600048', 'SH600039', 'SH600036', 'SH600028', 'SH600016',
              'SH600015', 'SZ002555', 'SZ002466', 'SZ002027', 'SZ000983', 'SZ000895', 'SZ000425', 'SZ000408',
              'SZ000002', 'SH600019', 'SH600900', 'SH600050', 'SH600519', 'SZ002714']
# 牧原股份SZ002714，双汇发展SZ000895

ball.set_token(f'xq_a_token={token}')

for stock in stock_list:
    # 10年的数据
    res = ball.kline(stock, 7300)['data']
    ll = res['item']
    klines = []
    for item in ll:
        dt = get_time(item[0])
        volume = item[1]
        open = item[2]
        high = item[3]
        low = item[4]
        close = item[5]
        change = item[6]
        change_percent = item[7]
        turnover_rate = item[8]
        amt = item[9]
        pe = item[12]
        pb = item[13]
        ps = item[14]
        pcf = item[15]
        market_capital = item[16]
        stock_code = stock
        kline = KLine(stock_code=stock_code, dt=dt, stock_volume=volume, open=open, high=high, low=low, close=close,
                      change=change, change_percent=change_percent, turnover_rate=turnover_rate,
                      transaction_amt=amt, pe=pe, pb=pb, ps=ps, pcf=pcf, market_capital=market_capital)
        klines.append(kline)
    insert(klines)
    print(res)
