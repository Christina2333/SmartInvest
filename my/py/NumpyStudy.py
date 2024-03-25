import numpy as np
import pandas as pd
from collections import OrderedDict


# list和array区别：list可以放置不同类型元素，array中元素类型必须一致
# array和Series：Series有索引，array没有

def test_numpy_one_dim():
    a = np.array([1, 2, 3, 4, 5])
    print(a[0])
    print(a[-1])
    print(a[1:3])
    print(a.dtype)
    print(a.mean())
    print(a.std())
    b = np.array([1, 2, 3])
    print(b * 4)


def test_numpy_two_dim():
    a = np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ])
    # 获取单个坐标或者行列
    print(a[0, 2])
    print(a[0, :])
    print(a[:, 0])
    # 分组
    print(a.mean(axis=1))  # 1表示按行分组
    print(a.mean(axis=0))  # 0表示按列分组


if __name__ == '__main__':
    test_numpy_two_dim()
