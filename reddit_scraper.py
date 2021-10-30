import config
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

    # Load stock {ticker, name} from csv:

    start = dt.datetime(2020, 1, 1, 0, 0, 0)
    one_day = dt.timedelta(days=1)
    while start.year < 2021:
        start_epoch = int(start.timestamp())
        end = start + one_day
        end_epoch = int(end.timestamp())
        # print(start)
        # print(start_epoch)
        # print(end)
        # print(end_epoch)


        start = end

    # submissions = list(ps_reddit.search_submissions(subreddit="wallstreetbets", after=start, before=end, limit=5))
    # for submission in submissions:
    #     print("Submission: " + submission.selftext)
    #     print("Score: " + str(submission.score))
    #     print("Date: " + str(submission.created_utc))
    #     for comment in submission.comments.list():
    #         print("Comment: " + comment.body)


if __name__ == '__main__':
    main()
