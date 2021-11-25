"""
    File name: scrape.py
    Authors: Dang Nguyen, Jonathan Birkey, Mathew McDade, Sakshi Maheshwari
    Emails: dangn2@illinois.edu, jbirke2@illinois.edu, mmcdade2@illinois.edu, smahes20@illinois.edu
    Python Version: 3.10.0
"""
import click
import configparser
import csv
import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import praw
from psaw import PushshiftAPI
from statistics import mean
import sys
import time
from tqdm import tqdm

# Global variables
CONFIG_FILE = "config.ini"
OUTPUT_JSON_FILE = "output.json"
SUBREDDIT = "wallstreetbets"


def check_for_files(file):
    """Ensures config file is present before running

    :param file: The file to check if exists
    :type file: str
    :return: bool
    :rtype: bool
    """
    try:
        with open(file, "r") as f:
            pass
        return True
    except FileNotFoundError:
        print(f"ERROR: could not find \"{file}\"\nPlease make sure it is in your local directory")
        return False


def format_period_yahoo(period):
    """Formats the period into an int representation for the Yahoo Finance API

    :param period: The datetime passed in from the CLI
    :type period: datetime
    :return: period
    :rtype: int
    """
    return int(time.mktime(datetime.datetime.timetuple(period)))


def query_yahoo_finance_api(symbol, period_start, period_end, period_interval):
    """Returns a dataframe from the stock symbol containing stock data over from period start to period end

    :param symbol: the stock ticker symbol
    :type symbol: str
    :param period_start: date of the beginning of the period
    :type period_start: int
    :param period_end: date of the end of the period
    :type period_end: int
    :param period_interval: the interval of stock data over the period
    :type period_interval: str
    :return: stock_data
    :rtype: pd.DataFrame
    """
    yahoo_api = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period_start}&" \
                f"period2={period_end}&interval={period_interval}&events=history&includeAdjustedClose=true"
    return pd.read_csv(yahoo_api)


def get_dates_in_period(period_start, period_end, period_interval):
    """Returns a list of all the trading dates within the period_start and period_end

    :param period_start: date of the beginning of the period
    :type period_start: int
    :param period_end: date of the end of the period
    :type period_end: int
    :param period_interval: the interval of stock data over the period
    :type period_interval: str
    :return: dates
    :rtype: list[str]
    """
    df = query_yahoo_finance_api("MMM", period_start, period_end, period_interval)
    return df["Date"].values


def get_csv_data(file):
    """Returns the first row of a csv file as a list of strings

    :param file: path to the csv file that contains the data to build the list from
    :type file: str
    :return: csv_data
    :rtype: list[str]
    """
    csv_data = []
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip csv file headers
        for i in reader:
            csv_data.append(i[0])
    return csv_data


def build_json_template(symbols, dates, file):
    """Builds the json file template

    :param symbols: list of stock ticker symbols
    :type symbols: list[str]
    :param dates: list of dates
    :type dates: list[str]
    :param file: path to the etf csv file
    :type file: str
    :return: None
    """
    json_schema = {}
    i = 0
    while i < len(symbols):
        symbol_entry = {symbols[i]: ""}
        date_entry = {}
        j = 0
        while j < len(dates):
            date_entry.update({dates[j]: {"stock_data": {}, "reddit_data": {}}})
            j += 1
        symbol_entry.update({symbols[i]: date_entry})
        json_schema.update(symbol_entry)
        i += 1
    with open(file, "w") as f:
        json.dump(json_schema, f)


def calculate_daily_change_rate(df):
    """Calculates the change and change rate for each date in the data frame df

    :param df: The data from encoding stock data by date for a given stock
    :type df: pd.DataFrame
    :return: None
    """
    df['Change'] = np.subtract(df['Close'].values, df['Open'].values)
    df['Change Rate'] = np.divide(df['Change'].values, df['Open'].values)


def update_stock_data_in_json(symbol, df):
    """Populate json file template with stock pricing data

    :param symbol: the stock ticker symbol of the DataFrame
    :type symbol: str
    :param df: post-processed DataFrame
    :type df: pd.DataFrame
    :return: None
    """
    with open(OUTPUT_JSON_FILE, "r") as f:
        json_data = json.load(f)

    for row in df.values:
        date = row[0]
        stock_data_entry = {
            "Open": row[1],
            "High": row[2],
            "Low": row[3],
            "Close": row[4],
            "Adj Close": row[5],
            "Volume": row[6],
            "Change": row[7],
            "Change Rate": row[8]
        }
        json_data[symbol][str(date)].update({"stock_data": stock_data_entry})

    with open(OUTPUT_JSON_FILE, "w") as f:
        json.dump(json_data, f)


def update_reddit_data_in_json(symbol, dates):
    """Populate json file template with stock reddit data

    :param symbol: the stock ticker symbol to search reddit for
    :type symbol: str
    :param dates: list of all trading dates in period
    :type dates: list[str]
    :return: None
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config_id = config.get("reddit", "client_id")
    config_secret = config.get("reddit", "client_secret")
    config_agent = config.get("reddit", "user_agent")
    reddit = praw.Reddit(client_id=config_id, client_secret=config_secret, user_agent=config_agent)
    reddit_api = PushshiftAPI(reddit, shards_down_behavior=None)

    with open(OUTPUT_JSON_FILE, "r") as f:
        json_data = json.load(f)

    for date in tqdm(dates, desc=symbol, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} \t\t\t\t", dynamic_ncols=True):
        reddit_data_entry = {
            "comments": []
        }
        reddit_start = datetime.datetime.strptime(date, "%Y-%m-%d")
        reddit_end = reddit_start + datetime.timedelta(days=1)
        reddit_start = int(reddit_start.timestamp())
        reddit_end = int(reddit_end.timestamp())
        comments = list(
            reddit_api.search_comments(subreddit=SUBREDDIT, q=symbol, after=reddit_start, before=reddit_end))
        for comment in comments:
            comment_entry = {
                "author": comment.author.name.encode("ascii", "ignore").decode() if comment.author else "",
                "body": comment.body if comment.body else "",
                "score": comment.score if comment.score else 0
            }
            comment_entry['body'] = comment_entry['body'].encode("ascii", "ignore").decode()
            comment_entry['body'] = comment_entry['body'].replace("*", " ")
            comment_entry['body'] = comment_entry['body'].replace("\n", " ")
            comment_entry['body'] = comment_entry['body'].replace("\"", " ")
            comment_entry['body'] = ' '.join(comment_entry['body'].split())
            reddit_data_entry["comments"].append(comment_entry)
        json_data[symbol][str(date)].update({"reddit_data": reddit_data_entry})
        time.sleep(2)  # sleep to avoid abusing the API
    with open(OUTPUT_JSON_FILE, "w") as f:
        json.dump(json_data, f)


def get_comment_score(comments, score_type='avg'):
    """Return overall score value for the input comments list

    :param comments: comments list
    :type comments: list[dict]
    :param score_type: min/max/avg/sum/first (where 'first' means just return score of the first comment)
    :type score_type: str
    :return: overall score value
    :rtype: float
    """
    if score_type == 'first':
        return comments[0]['score']
    elif score_type == 'min':
        return min([comment['score'] for comment in comments])
    elif score_type == 'max':
        return max([comment['score'] for comment in comments])
    elif score_type == 'sum':
        return sum([comment['score'] for comment in comments])
    else:  # include 'avg' and any other score_type
        return mean([comment['score'] for comment in comments])


@click.command(name="get")
@click.option("--interval", "-i", type=click.Choice(["1d", "1wk", "1mo"], case_sensitive=False), default="1d")
@click.argument("start", type=click.DateTime())
@click.argument("end", type=click.DateTime())
@click.argument("stocks", type=click.Path(exists=True))
def get_data(interval, start, end, stocks):
    """Get data for all stocks in csv from start to end at interval
    """
    if not check_for_files(CONFIG_FILE):
        sys.exit()
    yahoo_start = format_period_yahoo(start)
    yahoo_end = format_period_yahoo(end)
    symbols = get_csv_data(stocks)
    dates = get_dates_in_period(yahoo_start, yahoo_end, interval)
    build_json_template(symbols, dates, OUTPUT_JSON_FILE)
    for symbol in symbols:
        df = query_yahoo_finance_api(symbol, yahoo_start, yahoo_end, interval)
        calculate_daily_change_rate(df)
        update_stock_data_in_json(symbol, df)
    for symbol in symbols:
        update_reddit_data_in_json(symbol, dates)


@click.command(name="chart")
@click.argument("dataset", type=click.Path(exists=True))
@click.argument("symbol")
@click.option("--score_type", "-t", type=click.Choice(["max", "min", "avg", "sum", "first"], case_sensitive=False),
              default="avg")
def chart_data(dataset, symbol, score_type):
    """Chart the data for the stock
    """
    with open(dataset) as f:
        web_data = json.load(f)

    stock_price = []
    reddit_score = []
    no_reddit_count = 0

    for key in web_data[symbol].keys():
        num_of_comments = len(web_data[symbol][key]['reddit_data']['comments'])
        # Only plot chart on the day that has reddit comment
        if num_of_comments > 0:
            stock_price.append([key, round(float(web_data[symbol][key]['stock_data']['Close']), 2)])
            reddit_score.append([key, round(float(get_comment_score(web_data[symbol][key]['reddit_data']['comments'],
                                                                    score_type)), 2)])
        else:
            no_reddit_count += 1

    # Check plot data before plot. Exit if no data.
    stock_data_count = len(web_data[symbol].keys())
    reddit_data_count = stock_data_count - no_reddit_count
    print("Total stock data count:", stock_data_count)
    print("Total reddit data count:", reddit_data_count)
    if reddit_data_count == 0 or stock_data_count == 0:
        print('No data for plotting. Exit!')
        exit(0)

    df1 = pd.DataFrame(stock_price, columns=["Day", "Stock_Price"])
    df2 = pd.DataFrame(reddit_score, columns=["Day", "Reddit_Score"])

    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    df1.plot(x="Day", y=["Stock_Price"], ax=ax, label=['Stock Price'])
    ax.legend(loc='upper left')
    df2.plot(x="Day", y=["Reddit_Score"], ax=ax2, ls="--", color='gray', label=['Reddit Score'])
    ax2.legend(loc='upper right')
    plt.title("Correlation Chart - Symbol=" + symbol, loc='center')
    plt.show()


@click.group()
def cli():
    pass


cli.add_command(get_data)
cli.add_command(chart_data)

if __name__ == "__main__":
    cli()
