"""
    File name: stock_scrapper.py
    Author: Jonathan Birkey
    Email: jbirke2@illinois.edu
    Date created: 29 Oct 2021
    Python Version: 3.10.0
    Notes: S&P 500 company list pulled from https://datahub.io/core/s-and-p-500-companies#data
"""
import csv
import datetime
import numpy as np
import pandas as pd
import time


def get_sp500_tickers(file: str) -> list[str]:
    tickers = []
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip csv file headers
        for i in reader:
            tickers.append(i[0])
    return tickers


def calculate_daily_change_rate(df: pd.DataFrame) -> None:
    df['Change'] = np.zeros((len(df)))
    df['Change Rate'] = np.zeros((len(df)))
    for i in df.index:
        df['Change'].iloc[i] = (df['Close'].iloc[i] - df['Open'].iloc[i])
        df['Change Rate'].iloc[i] = (df['Close'].iloc[i] - df['Open'].iloc[i]) / df['Open'].iloc[i] * 100


def main():
    file_path = 'data/sp_500_constituents_as_of_20211022.csv'
    tickers = get_sp500_tickers(file_path)
    ticker = 'MMM'
    period1 = int(time.mktime(datetime.datetime(2020, 1, 1, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2020, 12, 31, 23, 59).timetuple()))
    interval = '1d'  # daily = 1d, weekly = 1wk, monthly = 1m

    query_str = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&' \
                f'period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

    df = pd.read_csv(query_str)
    calculate_daily_change_rate(df)

    # TODO: calculate change and change rate for every ticker in the tickers list and save it as a single dataset


if __name__ == "__main__":
    main()
