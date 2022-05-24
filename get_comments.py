import praw
import numpy as np
import time
import pandas as pd
import requests
import re

"""
    Download all comments in a list of posts
"""


def request_json(url):
    while True:
        try:
            r = requests.get(url)
            if r.status_code != 200:
                print('error code', r.status_code)
                time.sleep(5)
                continue
            else:
                break
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
    return r.json()


def get_comment_for_post(post_id, post_time, post_title):
    tmp = []

    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=None)

    for comment in submission.comments.list():

        tmp.append({
            'post_id': post_id,
            'post_time': post_time,
            'post_title': post_title,
            'comment_id': comment.id,
            'comment_time': comment.created_utc,
            'comment_body': format_str(comment.body),
            'comment_author': comment.author,
        })

        if TIMEOUT_AFTER_COMMENT_IN_SECS > 0:
            time.sleep(TIMEOUT_AFTER_COMMENT_IN_SECS)

    return tmp


def format_str(in_str):
    tmp = re.sub('[^a-zA-Z0-9 ]+', ' ', in_str)  # remove weird characters
    return re.sub(' +', ' ', tmp)  # remove double spaces


TIMEOUT_AFTER_COMMENT_IN_SECS = .350
subreddit = 'Europe'
TIMESTAMP = '1653044298'

reddit = praw.Reddit(client_id="TSKXaE564OHiEEN_90ofOQ",  # your client id
                     client_secret="VRcPIrXH0UXqpoaVYTxiq5ZjWwOJmg",  # your client secret
                     user_agent="soc-comp")  # your user agent

df = pd.read_csv(subreddit + '_filtered_submission_' + TIMESTAMP + '.csv')

totalResults = df.shape[0]

startTime = time.time()
timePrint = startTime

meta = request_json('https://api.pushshift.io/meta')
limitPerMinute = meta['server_ratelimit_per_minute']
requestWait = 60 / limitPerMinute
printWait = 2
i = 0

with open(subreddit + '_comment_' + str(int(time.time())) + '_' + TIMESTAMP + '.csv', 'w', encoding="utf-8") as f:
    # Write header
    f.write('post_id,post_time,post_title,comment_id,comment_time,comment_body,comment_author\n')

    print('\n[starting downloading comments]')

    for index, row in df.iterrows():
        comment_list = get_comment_for_post(row['id'], row['time'], row['title'])

        for item in comment_list:
            f.write("{},{},{},{},{},{},{}\n".format(
                item['post_id'],
                item['post_time'],
                item['post_title'],
                item['comment_id'],
                item['comment_time'],
                item['comment_body'],
                item['comment_author'],
            ))

        i += 1

        if time.time() - timePrint > printWait:
            timePrint = time.time()
            percent = i / totalResults * 100

            timePassed = time.time() - startTime

            print('{:.2f}'.format(percent) + '%', '|', time.strftime("%H:%M:%S", time.gmtime(timePassed)))

            time.sleep(requestWait)
