import pandas as pd


df = pd.read_csv('sentiment_scores_1655707345_1655215516.csv')

print(len(df['comment_author'].unique().tolist()))

df['comment_author'] = df['comment_author'].astype('category').cat.codes

length = len(df)//2

df_1 = df[:length]
df_2 = df[length:]

df_1.to_csv('all_posts_1.csv', index=False, sep=';')
df_2.to_csv('all_posts_2.csv', index=False, sep=';')

