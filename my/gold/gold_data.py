import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('../data/commodity/518880.SS.csv').set_index('Date')
plt.plot(df.index, df['Close'])