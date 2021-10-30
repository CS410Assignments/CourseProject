from collections import defaultdict
import config
import json
import pandas as pd
import numpy as np
import praw
from psaw import PushshiftAPI
import datetime as dt
from time import sleep


def main():
    reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                         user_agent=config.user_agent)
    print(reddit.read_only)
    # wsb = reddit.subreddit("wallstreetbets")
    # print(wsb.display_name)
    # print(wsb.title)
    # print(wsb.description)
    ps_reddit = PushshiftAPI(reddit)

    documents = dict()

    # Load stock {ticker, name} from csv:
    stocks = pd.read_csv("data/sp_500_constituents_as_of_20211022.csv")
    for _, stock in stocks.iterrows():
        # print(stock['Symbol'], stock['Name'])
        documents[stock['Symbol']] = dict()
        start = dt.datetime(2020, 1, 1, 0, 0, 0)
        one_day = dt.timedelta(days=1)
        while start.year < 2021:
            start_epoch = int(start.timestamp())
            end = start + one_day
            end_epoch = int(end.timestamp())

            documents[stock['Symbol']][start.strftime("%d%b%Y")] = dict()
            documents[stock['Symbol']][start.strftime("%d%b%Y")]['reddit_data'] = dict()
            documents[stock['Symbol']][start.strftime("%d%b%Y")]['reddit_data']['submissions'] = list()
            test_submission = {
                'id': "",
                'self_text': "",
                'score': 0,
                'upvote_ratio': 0,
                'num_comments': 0,
                'comments': list()
            }
            test_comment = {
                'self_text': "",
                'score': 0
            }
            test_submission['comments'].append(test_comment)
            documents[stock['Symbol']][start.strftime("%d%b%Y")]['reddit_data']['submissions'].append(test_submission)
            # print(start)
            # print(start_epoch)
            # print(end)
            # print(end_epoch)
            # documents[stock['Symbol']][start]['reddit_data']['submissions'] = {}
            # submissions = list(ps_reddit.search_submissions(subreddit="wallstreetbets", after=start, before=end, limit=5))
            # for submission in submissions:
            #     print("Submission: " + submission.selftext)
            #     print("Score: " + str(submission.score))
            #     print("Date: " + str(submission.created_utc))
            #     for comment in submission.comments.list():
            #         print("Comment: " + comment.body)
            start = end
            # sleep to avoid abusing the API
            # sleep(2)
    with open('documents.json', 'w+') as documents_file:
        json.dump(documents, documents_file)
    # print(documents)


if __name__ == '__main__':
    main()
