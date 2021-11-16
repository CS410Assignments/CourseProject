import matplotlib.pyplot as plt
import json
import pandas as pd
from statistics import mean


def max_value(comments) -> int:
    return max([comment['score'] for comment in comments])


def avg_value(comments) -> float:
    return mean([comment['score'] for comment in comments])


def sum_value(comments) -> float:
    return sum([comment['score'] for comment in comments])


def min_value(comments) -> float:
    return min([comment['score'] for comment in comments])


def main(multi_ticker_dataset=True, ticker="AMZN"):

    if multi_ticker_dataset:
        input_file = 'data/cleaned_team_yoda_data_stocks_with_comments.json'
    else:
        input_file = 'data/' + ticker + '_team_yoda_data.json'

    with open(input_file) as f:
        web_data = json.load(f)

    stock_price = []
    reddit_score = []
    no_reddit_count = 0

    for key in web_data[ticker].keys():
        num_of_comments = len(web_data[ticker][key]['reddit_data']['comments'])
        if num_of_comments > 0:
            stock_price.append([key, round(float(web_data[ticker][key]['stock_data']['Close']), 2)])
            # use avg score of comments for the key(i.e. day)
            reddit_score.append([key, round(float(avg_value(web_data[ticker][key]['reddit_data']['comments'])), 2)])
        else:
            no_reddit_count += 1

    # Check plot data before plot. Exit if no data.
    stock_data_count = len(web_data[ticker].keys())
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

    df1.plot(x="Day", y=["Stock_Price"], ax=ax)
    df2.plot(x="Day", y=["Reddit_Score"], ax=ax2, ls="--")
    plt.title("Correlation Chart - Ticker=" + ticker, loc='center')
    plt.show()


if __name__ == "__main__":
    # Call the main(multi_ticker_dataset=Boolean, ticker=String) function to read data and show the plot
    # multi_ticker_dataset: True; use the all-tickers dataset file. False; use single-ticker dataset
    # ticker: ticker to be plotted
    # If not provided, default values for def main(multi_ticker_dataset=True, ticker="AMZN")
    main(True, ticker="AMC")
