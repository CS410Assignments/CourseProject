import config
import json
import pandas as pd
import praw
from psaw import PushshiftAPI
import datetime as dt
from time import sleep

SUBREDDIT = "wallstreetbets"

def main():
    reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                         user_agent=config.user_agent)
    print(reddit.read_only)
    ps_reddit = PushshiftAPI(reddit)

    documents_data = None
    with open('data/team_yoda_data.json', 'r') as documents_file:
        documents_data = json.load(documents_file)

    # Load stock {Symbol, Name} from csv:
    stocks = pd.read_csv("data/fomo_etf_as_of_20211031.csv")

    for _, stock in stocks.iterrows():
        print(stock['Symbol'] + " " + stock['Name'])
        start = dt.datetime(2020, 1, 2, 0, 0, 0)
        print(start.strftime("%Y-%m-%d"))
        one_day = dt.timedelta(days=360)
        while start.year < 2021:
            end = start + one_day
            if start.strftime("%Y-%m-%d") not in documents_data[stock['Symbol']]:
                start = end
                continue
            start_epoch = int(start.timestamp())
            end_epoch = int(end.timestamp())

            documents_data[stock['Symbol']][start.strftime("%Y-%m-%d")]['reddit_data']['submissions'] = list()

            submissions = list(
                ps_reddit.search_submissions(subreddit=SUBREDDIT, q=stock['Symbol'], after=start_epoch, before=end_epoch, limit=10))
            for submission in submissions:
                submission_item = {
                    'author': submission.author.name if submission.author else "",
                    'selftext': submission.selftext if submission.selftext else "",
                    'score': submission.score if submission.score else 0,
                    'upvote_ratio': submission.upvote_ratio if submission.upvote_ratio else 0.0,
                    'num_comments': submission.num_comments if submission.num_comments else 0,
                    'comments': list()
                }
                for comment in submission.comments.list():
                    comment_item = {
                        'author': comment.author.name if comment.author else "",
                        'body': comment.body if comment.body else "",
                        'score': comment.score if comment.score else 0
                    }
                    submission_item['comments'].append(comment_item)
                documents_data[stock['Symbol']][start.strftime("%Y-%m-%d")]['reddit_data']['submissions'].append(submission_item)

            start = end
            # sleep to avoid abusing the API
            sleep(3)

    with open('data/team_yoda_data.json', 'w+') as documents_file:
        json.dump(documents_data, documents_file)


if __name__ == '__main__':
    main()
