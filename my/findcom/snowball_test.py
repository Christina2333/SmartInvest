import pysnowball as ball
import pandas as pd
import json

ball.set_token('xq_a_token=a803f604aa4e3ac6eda2cab6cdb26a76b83f4c04')


# df = pd.read_excel('../data/usa/标普500成分股.xlsx')
df = pd.read_excel('../data/usa/纳指100成分股.xlsx')

for index, row in df.iterrows():
    stock_id = row['股票代号']
    stock_name = row['公司']
    company_class = row['全球行业分类标准部门']
    company_class_2 = row['全球行业分类标准子行业']
    join_in_time = row['加入日期']
    start_time = row.get('成立年份')
    res = ball.quote_detail(stock_id)
    res = res['data']['quote']
    json_str = json.dumps(res)
    if 25 > res['pe_ttm'] > 0:
        print(f"股票代号:{stock_id},公司名为:{stock_name},分类为:{company_class}/{company_class_2},加入日期:{join_in_time},公司成立年份:{start_time}")
        # 每股收益
        print(f"每股收益:{res['eps']},预测pe:{res['pe_forecast']},pe_lyr:{res['pe_lyr']},pe_ttm:{res['pe_ttm']}")
        print()

'''
0.股价估值模型学习
1.选择几个指标来恒量一个公司，例如市盈率，毛利率等
2.把雪球接口和返回值和具体的指标对应起来
3.利用程序爬取复合条件的公司，看财报
'''



