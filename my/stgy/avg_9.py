import pandas as pd
import matplotlib.pyplot as plt


def avg_9_stgy(data, params):
    """
    @param data:
    @param params:
    """
    r1 = params['r1']
    r2 = params['r2']
    # 10日均线
    data_r1 = data.rolling(window=r1).mean()
    # 28日均线
    data_r2 = data.rolling(window=r2).mean()
    target_wgt = pd.DataFrame(data=0, index=data.index, columns=data.columns)
    avg_9 = pd.DataFrame(data=0, index=data.index, columns=data.columns)

    for i in range(len(data) - 4):
        for k in range(9):
            if i + k + 4 < len(data):
                if data.iloc[i + k]['Close'] < data.iloc[i + k + 4]['Close']:
                    avg_9.iloc[i]['Close'] = 9-k
                # else:
                    # for idx in range(k):
                    #     avg_9.iloc[i - idx] = 0

    pd.set_option('display.max_rows', None)
    print(avg_9)

    for idx in range(len(data) - 4):
        r1_row = data_r1.iloc[idx]
        r1_last_row = data_r1.iloc[idx - 1]
        r2_row = data_r2.iloc[idx]
        r2_last_row = data_r2.iloc[idx - 1]
        avg = avg_9.iloc[idx]
        avg_last = avg_9.iloc[idx - 1]
        if r1_row['Close'] is not None and r2_row['Close'] is not None:
            if r1_row['Close'] >= r2_row['Close'] and r1_last_row['Close'] <= r2_last_row['Close']:
                if avg['Close'] > 0:
                    target_wgt.iloc[idx] = 1
            elif r1_row['Close'] > r2_row['Close'] and avg_last['Close'] is not None and avg_last['Close'] > 0:
                target_wgt.iloc[idx] = 1

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(data['Close'], label='net value')
    ax1.plot(data_r1['Close'], label='10')
    ax1.plot(data_r2['Close'], label='28')
    ax1.legend()

    ax2 = fig.add_subplot(212)
    ax2.plot(avg_9['Close'], label='9')
    ax2.plot(target_wgt['Close'], label='hold')
    ax2.legend()
    plt.tight_layout()
    plt.show()
    return target_wgt
