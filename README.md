# CourseProject

## Dataset Link
https://drive.google.com/file/d/1wc70jYnUfgGiHCInkFQqTbkFTqTNygsz/view?usp=sharing

## Tutorial
Please fork this repository and paste the GitHub link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

1. Clone repo
2. In same directory run `pip3 install .`
3. Run CLI app by running `% scrape get [interal option | 1d, 1wk, 1mo] <period start | yyyy-mm-dd> <period end | yyyy-mm-dd> <path to stocks csv file> <path to reddit api config text file>`
4. Example `% scrape get 2020-01-01 2020-12-31 data/test_stocks.csv config.txt`
5. This will produce `output.json` in your local directory
6. Run CLI app to chart data `% scrape chart <path to output.json> <ticker symbol>`
7. Example `% scrape chart output.json TSLA`

## Stocks.csv

### Format
```text
Symbol,Name  
stock symbol 1,stock name 1  
stock symbol 2,stock name 2  
stock symbol 3,stock name 3
```

### Example
```text
Symbol,Name  
AMC,AMC Entertainment Holdings Inc. Cl A  
LC,LendingClub Corp.  
COST,Costco Wholesale Corp.
```

## Config.ini

### Format
```ini
[section name]
client_id = client_id  
client_secret = client_secret  
user_agent = user_agent
```

### Example
```ini
[reddit]
client_id = nW2n_31gApdn
client_secret = dfopabA323BaSDBFa
user_agent = UserName
```
