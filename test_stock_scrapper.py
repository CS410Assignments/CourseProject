import json
import pathlib as pl
import pandas as pd
import unittest
import stock_scrapper


class TestStockScrapper(unittest.TestCase):
    d = {'Date': ['2020-01-02', '2020-01-03', '2020-01-06'], 'Open': [7.30, 7.45, 7.25], 'High': [7.31, 7.46, 7.26],
         'Low': [7.29, 7.44, 7.26], 'Close': [7.30, 7.00, 8.00], 'Adj Close': [7.30, 7.45, 7.25],
         'Volume': [4545900, 2218000, 2903400]}
    test_df = pd.DataFrame(data=d)
    csv_path = pl.Path('data/fomo_etf_as_of_20211031.csv')
    json_path = pl.Path('data/Team_yoda_dataSet.json')
    ticker = 'MMM'

    def test_get_fomo_tickers(self):
        test_array = stock_scrapper.get_fomo_tickers(self.csv_path)
        self.assertEqual(len(test_array), 25)
        self.assertEqual(test_array[4], "GME")

    def test_calculate_daily_change_rate(self):
        self.assertTrue(stock_scrapper.calculate_daily_change_rate(self.test_df))
        # Have to round list element to fix floating point error
        self.assertListEqual(list(self.test_df['Change'].round(10)), [0., -0.45, 0.75])

    def test_build_stock_json(self):
        self.assertTrue(self.json_path)
        with open(self.json_path) as json_file:
            content = json.load(json_file)
        self.assertEqual(int(content['GME']['2020-05-05']['stock_data']['Volume']), 2105900)
        self.assertTrue('AMC' in content)
        self.assertTrue('2020-07-10' in content['AMC'])
        self.assertTrue('stock_data' in content['AMC']['2020-07-10'])
        self.assertTrue('reddit_data' in content['AMC']['2020-07-10'])
        self.assertTrue('Change' in content['AMC']['2020-07-10']['stock_data'])
        self.assertTrue('Change Rate' in content['AMC']['2020-07-10']['stock_data'])


if __name__ == '__main__':
    unittest.main()
