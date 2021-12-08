# <b>CS410 - Final Project Report</b>

## <b>Team Reddit Recommenders</b>

Nico Calderon nac7@illinois.edu</br>
Ethan Choi ethansc2@illinois.edu</br>
Kimberly Martin kjmarti2@illinois.edu</br>
Miguel Paulo Riano mriano2@illinois.edu</br>
Anthony Safo as95@illinois.edu (team coordinator)

## The following are the project file structure for the Reddit Recommenders:

<b>redditScraper.py</b> - code for scraping reddit and subreddits. This uses praw for retrieving data from reddit, and pandas for storing and arranging the relationship between reddit, subrreddit and submissions.</br></br>
<b>flask_main.py</b> - code for the web application, it uses flask library as the micro web framework</br></br>
<b>output-submissions.csv</b> - contains the submissions scraped from reddit in csv format, comma delimited</br></br>
<b>output-submissions.xml</b> - contains the submissions scraped from reddit in xml format</br></br>
<b>output-subreddits.csv</b> - contains the subreddits scraped from reddit in csv format, comma delimited</br></br>
<b>ranker.py</b> - code for doing the ranking calculations of the pulled reddit/subrredit</br></br>
<b>results.csv</b> - contains the results for the ranked filed</br>

## Module Details

### 1. Scraper Module</br>

- <b>Description</b>: The scaper module is responsible for scraping reddit, subreddits and its submissions. In this module we are using libraries praw and pandas. Praw is the main library to scrape the tool and pandas for manipulating the retrieved data. Authentication is done via client id, and client secret and user id and password.</br>

- The code file for this module is redditScraper.py

- <b>Usage</b>: to use this tool, simple type "python redditScraper.py -l1 10 -l2 10"

-- The first parameter "-l1" is the number of subreddits you want to scrape. The default is 5, and you can put any integer value
-- The second parameter "-l2" is the number of submissions you want to scrape. The default is 5, and you can put any integer value

### 2. Ranker Module</br>

- <b>Description</b>: 
- <b>Usage</b>: 

### 3. UI/Flask Module</br>

- <b>Description</b>: 
- <b>Usage</b>:
