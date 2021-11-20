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
    with open('data/team_yoda_data_stocks_pre_comments.json', 'r') as documents_file:
        documents_data = json.load(documents_file)

    # Load stock {Symbol, Name} from csv:
    stocks = pd.read_csv("data/fomo_etf_as_of_20211031.csv")

    for _, stock in stocks.iterrows():
        print(stock['Symbol'] + " " + stock['Name'])
        query = stock['Symbol']
        start = dt.datetime(2020, 1, 2, 0, 0, 0)
        one_day = dt.timedelta(days=1)
        while start.year < 2021:
            print(start.strftime("%Y-%m-%d"))
            end = start + one_day
            if start.strftime("%Y-%m-%d") not in documents_data[stock['Symbol']]:
                start = end
                continue
            start_epoch = int(start.timestamp())
            end_epoch = int(end.timestamp())

            documents_data[stock['Symbol']][start.strftime("%Y-%m-%d")]['reddit_data']['comments'] = list()

            comments = list(
                ps_reddit.search_comments(subreddit=SUBREDDIT, q=query, after=start_epoch, before=end_epoch,
                                          sort_type="score", sort="desc", size=25))
            for comment in comments:
                comment_item = {
                    'author': comment.author.name.encode("ascii", "ignore").decode() if comment.author else "",
                    'body': comment.body if comment.body else "",
                    'score': comment.score if comment.score else 0
                }
                documents_data[stock['Symbol']][start.strftime("%Y-%m-%d")]['reddit_data']['comments'].append(
                    comment_item)

            start = end
            # sleep to avoid abusing the API
            sleep(2)
        with open('data/team_yoda_data_stocks_with_comments.json', 'w+') as documents_file:
            json.dump(documents_data, documents_file)


if __name__ == '__main__':
    main()
