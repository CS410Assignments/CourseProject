import datetime
import json
import os
import pandas as pd
import unittest
from scrape import scrape


class MyTestCase(unittest.TestCase):
    d = {'Date': ['2020-01-02', '2020-01-03', '2020-01-06'], 'Open': [7.30, 7.45, 7.25], 'High': [7.31, 7.46, 7.26],
         'Low': [7.29, 7.44, 7.26], 'Close': [7.30, 7.00, 8.00], 'Adj Close': [7.30, 7.45, 7.25],
         'Volume': [4545900, 2218000, 2903400]}
    test_df = pd.DataFrame(data=d)
    test_comment_list = [{"score": 1}, {"score": 2}, {"score": 3}, {"score": 4}]
    output_json_file = "test_output.json"
    test_csv_file = "test_stocks.csv"
    yahoo_period_start = 1577858400
    yahoo_period_end = 1609394400
    yahoo_interval = "1d"

    @classmethod
    def setUpClass(cls):
        with open(cls.output_json_file, "x") as f:
            pass

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.output_json_file)

    def test_check_for_files(self):
        self.assertFalse(scrape.check_for_files("fake_file.ini"))
        self.assertTrue(scrape.check_for_files("test.ini"))

    def test_format_period_yahoo(self):
        date = datetime.datetime(2020, 1, 1)
        result = scrape.format_period_yahoo(date)
        self.assertEqual(result, self.yahoo_period_start)
        date = datetime.datetime(2020, 12, 31)
        result = scrape.format_period_yahoo(date)
        self.assertEqual(result, self.yahoo_period_end)

    def test_query_yahoo_finance_api(self):
        result = scrape.query_yahoo_finance_api("MMM", self.yahoo_period_start, self.yahoo_period_end,
                                                self.yahoo_interval)
        self.assertEqual(result["Open"].size, 252)
        self.assertEqual(result.size, 1764)

    def test_get_dates_in_period(self):
        result = scrape.get_dates_in_period(self.yahoo_period_start, self.yahoo_period_end, self.yahoo_interval)
        self.assertEqual(len(result), 252)
        self.assertEqual(result[0], "2020-01-02")
        self.assertEqual(result[251], "2020-12-30")

    def test_get_csv_data(self):
        result = scrape.get_csv_data(self.test_csv_file)
        self.assertEqual(result[0], "GME")
        self.assertEqual(result[2], "WMT")
        self.assertEqual(result[3], "BRK-B")

    def test_build_json_template(self):
        symbols = ["GME", "TGT", "WMT"]
        dates = ["2020-01-01", "2020-01-02", "2020-01-06"]
        scrape.build_json_template(symbols, dates, self.output_json_file)
        with open(self.output_json_file, "r") as f:
            json_data = json.load(f)
        self.assertEqual(json_data["GME"]["2020-01-01"], {"stock_data": {}, "reddit_data": {}})
        self.assertEqual(json_data["GME"]["2020-01-02"], {"stock_data": {}, "reddit_data": {}})
        self.assertEqual(json_data["GME"]["2020-01-06"], {"stock_data": {}, "reddit_data": {}})

    def test_calculate_daily_change_rate(self):
        scrape.calculate_daily_change_rate(self.test_df)
        # Have to round list element to fix floating point error
        self.assertListEqual(list(self.test_df['Change'].round(10)), [0., -0.45, 0.75])


if __name__ == '__main__':
    unittest.main()
