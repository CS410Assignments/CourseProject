"""
    File name: stock_scrapper.py
    Author: Jonathan Birkey
    Email: jbirke2@illinois.edu
    Date created: 29 Oct 2021
    Python Version: 3.10.0
    Notes: S&P 500 company list pulled from https://datahub.io/core/s-and-p-500-companies#data
        FOMO ETF company list pulled from https://www.morningstar.com/etfs/bats/fomo/portfolio
    Task: Collect all the stock data from Yahoo finance and calculate daily change rate. 

    Author: Sakshi Maheshwari
    Email: smahes20@illinois.edu
    updated: Nov 3, 2021
    Task: Curate the collected data and store it in a JSON file. 

"""
import csv
import datetime
import json
import numpy as np
import os
import pandas as pd
import time


def build_stock_json(df: pd.DataFrame) -> dict:
    try:
        empty_js = {}
    
        # template for each ticker
        template = """{
            "%s" : {
                "stock_data" : {
                    "Open" : "%s",
                    "High": "%s",
                    "Low": "%s" ,
                    "Close": "%s",
                    "Adj Close": "%s",
                    "Volume": "%s",
                    "Change": "%s",
                    "Change Rate": "%s"
                },
                "reddit_data" : {
                    "submissions" : "TODO"
                }
            }
        }
        """
        for item in df.values:
            empty_js.update(json.loads(template%tuple(item.tolist())))
        return empty_js
    except BaseException as err:
        print(f'Something bad happened!: {err=}')
        return


def get_fomo_tickers(file: str) -> list[str]:
    tickers = []
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip csv file headers
        for i in reader:
            tickers.append(i[0])
    return tickers


def calculate_daily_change_rate(df: pd.DataFrame) -> bool:
    try:
        df['Change'] = np.subtract(df['Close'].values, df['Open'].values)
        df['Change Rate'] = np.divide(df['Change'].values, df['Open'].values)
        return True
    except BaseException as err:
        print(f'Something bad happened!: {err=}')
        return False


def main():
    file_path = 'data/fomo_etf_as_of_20211031.csv'

    # if the dataset file exists then delete file to avoid overwritting of data 
    output_path = 'data/team_yoda_data.json'
    if os.path.exists(output_path):
        os.remove(output_path)

    tickers = get_fomo_tickers(file_path)
    period1 = int(time.mktime(datetime.datetime(2020, 1, 1, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime(2020, 12, 31, 23, 59).timetuple()))
    interval = '1d'  # daily = 1d, weekly = 1wk, monthly = 1m
    file_data = {}  # initial empty dict to populate

    for ticker in tickers:
        query_str = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&' \
                    f'period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
        df = pd.read_csv(query_str)
        calculate_daily_change_rate(df)
        json_val = build_stock_json(df)
        file_data[ticker] = json_val

    with open(output_path,'a') as f:
        json.dump(file_data,f)


if __name__ == "__main__":
    main()


