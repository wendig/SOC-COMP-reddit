import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

"""
    Visualize stuff
"""


# Convert string to datetime
def date_convert(date_to_convert):
    return datetime.strptime(date_to_convert, '%Y-%m-%d')


# returns unique list while keeping its order
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [_x for _x in seq if not (_x in seen or seen_add(_x))]


df = pd.read_csv('sentiment_scores_1653061928_1653044298.csv')

print(df.columns)
print(df.head())

df['day'] = df['post_time'].str[:10]

df['datetime'] = df['day'].apply(date_convert)

df = df[df.datetime > datetime(2022, 1, 1)]

df = df.sort_values('datetime', ascending=True)

neg = df['neg'].groupby(df['day']).mean().values
neu = df['neu'].groupby(df['day']).mean().values
pos = df['pos'].groupby(df['day']).mean().values

x = np.array(f7(df['day'].values))

plt.plot(x, neg)

plt.plot(x, pos)

plt.plot(x, pos - neg, 'r+')

plt.xticks(rotation=45)

plt.show()
