import requests
import time
import datetime
import re

"""
    Download every post in the given subreddit
"""

subreddit = 'Europe'
maxThings = -1
printWait = 2
requestSize = 100


def format_str(in_str):
    return re.sub('[^a-zA-Z0-9 ]+', '', in_str)  # remove weird characters


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


meta = request_json('https://api.pushshift.io/meta')
limitPerMinute = meta['server_ratelimit_per_minute']
requestWait = 60 / limitPerMinute

print('server_ratelimit_per_minute', limitPerMinute)

thing = 'submission'

i = 0

print('Downloading: {}'.format(thing))

with open(subreddit + '_' + thing + '_' + str(int(time.time())) + '.csv', 'w', encoding="utf-8") as f:
    print('\n[starting', thing + 's]')

    if maxThings < 0:

        url = 'https://api.pushshift.io/reddit/search/' \
              + thing + '/?subreddit=' \
              + subreddit \
              + '&metadata=true&size=0'

        json = request_json(url)

        totalResults = json['metadata']['total_results']
        print('total ' + thing + 's', 'in', subreddit, ':', totalResults)
    else:
        totalResults = maxThings
        print('downloading most recent', maxThings)

    created_utc = ''

    startTime = time.time()
    timePrint = startTime

    f.write('time,title,full_link,permalink,score,id,subreddit_id' + '\n')

    while True:
        url = 'http://api.pushshift.io/reddit/search/' \
              + thing + '/?subreddit=' + subreddit \
              + '&size=' + str(requestSize) \
              + '&before=' + str(created_utc)

        json = request_json(url)

        if len(json['data']) == 0:
            break

        doneHere = False

        for post in json['data']:
            created_utc = post["created_utc"]

            needed = {
                'time': datetime.datetime.utcfromtimestamp(post['created_utc']).strftime('%Y-%m-%d %H:%M:%S'),
                'title': format_str(post['title']),
                'full_link': post['full_link'],
                'permalink': post['permalink'],
                'score': post['score'],
                'id': post['id'],
                'subreddit_id': post['subreddit_id']
            }
            f.write("{},{},{},{},{},{},{}\n".format(
                needed['time'],
                needed['title'],
                needed['full_link'],
                needed['permalink'],
                needed['score'],
                needed['id'],
                needed['subreddit_id'])
            )

            i += 1
            if i >= totalResults:
                doneHere = True
                break

        if doneHere:
            break

        if time.time() - timePrint > printWait:
            timePrint = time.time()
            percent = i / totalResults * 100

            timePassed = time.time() - startTime

            print('{:.2f}'.format(percent) + '%', '|', time.strftime("%H:%M:%S", time.gmtime(timePassed)))

        time.sleep(requestWait)
