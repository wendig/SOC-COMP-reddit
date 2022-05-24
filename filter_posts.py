import pandas as pd

"""
    Filter submission list based on a keyword in the title
"""


def filter_file(a, b, keyword):
    _df = pd.read_csv(a)

    print(_df.head())

    _df = _df.fillna('veryemptyrow')

    _df = _df.drop_duplicates()

    _df = _df[(_df.title.str.contains(keyword))]

    _df.to_csv(b, index=False)


old_file = 'Europe_submission_1653044298'
new_file = old_file.replace('submission', 'filtered_submission')

filter_file(old_file + '.csv', new_file + '.csv', 'migrant')
