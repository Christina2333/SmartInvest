from collections import OrderedDict

import pandas as pd


def test_pandas_one_dim():
    stocks = pd.Series([54.74, 190.9, 173.14, 1050.3, 181.86, 1139.49],
                       index=['腾讯', '阿里巴巴', '苹果', '谷歌', 'Facebook', '亚马逊'])
    print(stocks.describe())
    print(stocks.iloc[0])
    print(stocks.loc['腾讯'])
    # 向量运算
    s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
    s2 = pd.Series([10, 20, 30, 40], index=['a', 'b', 'e', 'f'])
    s3 = s1 + s2
    print(s3)
    # 删除空值
    print(s3.dropna())
    print(s1.add(s2, fill_value=0))


def test_pandas_two_dim():
    salesDict = {
        '日期': ['2018-08-01', '2018-08-02', '2018-08-03'],
        '社保卡号': ['001616528', '001616528', '001616528'],
        '商品编码': [236701, 236701, 236701],
        '商品名称': ['VC', '口服液', '感康'],
        '商品销量': [6, 1, 2],
        '实收金额': [82.8, 28, 16.8]
    }
    salesOrderedDict = OrderedDict(salesDict)
    salesDf = pd.DataFrame(salesOrderedDict)
    # 定位数据，裁剪
    # print(salesDf)
    # print(salesDf.mean(numeric_only=True))
    # print(salesDf.iloc[0, 3])
    # print(salesDf.iloc[0, :])
    # print(salesDf.iloc[:, 0])
    # print(salesDf.loc[0, '商品名称'])
    # print(salesDf.loc[0, :])
    # print(salesDf.loc[:, '商品名称'])
    # print(salesDf[['商品名称', '实收金额']])
    # print(salesDf.loc[:, '商品名称':'实收金额'])

    # 查询
    querySer = salesDf.loc[:, '商品销量'] > 1
    print(type(querySer))
    print(querySer)


if __name__ == '__main__':
    test_pandas_two_dim()