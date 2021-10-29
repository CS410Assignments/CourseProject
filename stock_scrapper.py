"""
    File name: stock_scrapper.py
    Author: Jonathan Birkey
    Email: jbirke2@illinois.edu
    Date created: 29 Oct 2021
    Python Version: 3.10.0
    Notes: S&P 500 company list pulled from https://datahub.io/core/s-and-p-500-companies#data
"""
import datetime
import pandas as pd
import time


def main():
    ticker = 'MMM'
    period1 = int(time.mktime(datetime.datetime(2020, 1, 1, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2020, 12, 31, 23, 59).timetuple()))
    interval = '1d'  # daily = 1d, weekly = 1wk, monthly = 1m

    query_str = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&' \
                f'period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    df = pd.read_csv(query_str)
    print(df)


if __name__ == "__main__":
    main()
