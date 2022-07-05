import nltk

"""
    Sentiment analysis with VADER model
"""

# Download only once
# nltk.download('vader_lexicon')
# nltk.download('stopwords')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import re
import demoji

# demoji.download_codes()

def format_str(in_str):
    return re.sub('[^a-zA-Z ]+', '', in_str)  # keep only letters


def remove_stop_words(in_str):
    _text = format_str(in_str)
    _text = _text.split(' ')
    _text = [word for word in _text if word.lower() not in stopwords.words('english')]
    return ' '.join(_text)


sid = SentimentIntensityAnalyzer()

a = 'This was a good movie.'
print(sid.polarity_scores(a))
a = 'This was the best, most awesome movie EVER MADE!!!'
print(sid.polarity_scores(a))
a = 'The acting was good , but the movie could have been better'
print(sid.polarity_scores(a))
a = 'WWIII is coming'
print(sid.polarity_scores(a))
a = 'The level of racism on this sub is in par with TD but not as dumb'
print(sid.polarity_scores(a))

import numpy as np
import pandas as pd

subreddit = 'Europe'
text_type = 'comment'
TIMESTAMPS = '1655707345_1655215516'

df = pd.read_csv('{}_{}_{}.csv'.format(subreddit, text_type, TIMESTAMPS), sep=';')

df.fillna('', inplace=True)

print(df.head())

polarities = {'neg': [], 'neu': [], 'pos': [], 'compound': []}

nr = df.shape[0]

for index, row in df.iterrows():
    # Extract emojis
    symbols = demoji.findall(row['comment_body'])
    # Remove stop words
    text = remove_stop_words(row['comment_body'])

    # If emojis are found add them at the end
    if bool(symbols):
        for key in symbols:
            text += ' ' + symbols[key]

    polarity = sid.polarity_scores(text)

    polarities['neg'].append(polarity['neg'])
    polarities['neu'].append(polarity['neu'])
    polarities['pos'].append(polarity['pos'])
    polarities['compound'].append(polarity['compound'])

    if index % 1000 == 0:
        print('Progress: {:0.2f} %'.format(index / nr * 100))

for key in polarities:
    df[key] = polarities[key]

print(df.head())

df.to_csv('sentiment_scores_{}.csv'.format(TIMESTAMPS), index=False)
