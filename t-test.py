import pandas as pd
from scipy import stats

df = pd.read_csv('sentiment_scores_1655707345_1655215516.csv').dropna(subset=['comment_body'])

df = df[df['comment_body'] != '[deleted]']

before_df = df[(df['post_time'] >= "2019-01-01") & (df['post_time'] <= "2021-12-31")]

after_df = df[(df['post_time'] >= "2022-01-31") & (df['post_time'] <= "2022-05-12")]

print(before_df.shape)
print(after_df.shape)
print(stats.ttest_ind(before_df['compound'], after_df['compound'], equal_var=False))