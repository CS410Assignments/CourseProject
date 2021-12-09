# <b>CS410 - Final Project Report</b>

## <b>Team Reddit Recommenders</b>

Nico Calderon nac7@illinois.edu</br>
Ethan Choi ethansc2@illinois.edu</br>
Kimberly Martin kjmarti2@illinois.edu</br>
Miguel Paulo Riano mriano2@illinois.edu</br>
Anthony Safo as95@illinois.edu (team coordinator)


<b>Overview</b>: A subreddit recommendation system where the user types a query pertaining to topics they are interested in, and the system uses the query and text data from the "hot" posts of the "top" active subreddits to recommend a list of subreddits to the user.


## The following are the project file structure for the Reddit Recommenders:

- <b>redditScraper.py</b> - code for scraping reddit and subreddits. This uses PRAW for retrieving data from reddit, and pandas for storing and arranging the relationship between reddit, subrreddit and submissions.</br></br>
- <b>flask_main.py</b> - code for the web application, it uses flask library as the micro web framework</br></br>
- <b>output-submissions.csv</b> - contains the submissions scraped from reddit in csv format, comma delimited</br></br>
- <b>output-submissions.xml</b> - contains the submissions scraped from reddit in xml format</br></br>
- <b>output-subreddits.csv</b> - contains the subreddits scraped from reddit in csv format, comma delimited</br></br>
- <b>ranker.py</b> - code for doing the ranking calculations of the pulled reddit/subrredit</br></br>
- <b>results.csv</b> - contains the results for the ranked filed</br>

## Module Details

### 1. Scraper Module</br>

- <b>Description</b>: The scaper module is responsible for scraping reddit, subreddits and its submissions. In this module we are using PRAW and pandas. PRAW is the Python Reddit API wrapper used to mine the text data from reddit. Pandas is the library used for manipulating the retrieved data. PRAW is installed via pip and requires a reddit account and creation of a reddit instance, whose authentication is done via client id, and client secret and user id and password.</br>

- The code file for this module is *redditScraper.py

- <b>Usage</b>: to use this tool, simply type "python redditScraper.py -l1 10 -l2 10"

  - The first parameter "-l1" is the number of subreddits you want to scrape. The default is 5, and you can put any integer value</br>
  - The second parameter "-l2" is the number of submissions you want to scrape. The default is 5, and you can put any integer value
  - Once it runs, it will generate the following files, *output-submissions.csv, *output-submissions.xml and *output-subreddits.csv

### 2. Ranker Module</br>

- <b>Description</b>: The ranker module is responsible for ranking the list of reddits and submissions retrieved. This is using BM25 as the main ranking function.
- The code file for this module is *ranker.py
- <b>Usage</b>: To run ranker.py type 'python ranker.py -n 10 -q "subreddit ranker"'
  - Edit 10 and "subreddit ranker" to be the number of results and the query, respectively.

### 3. UI/Flask Module</br>

- <b>Description</b>: The UI is done in HTML/CSS and the framework for the web application is Flask.
- The code file for this module is *flask_main.py
- <b>Usage</b>: to start the website, type python flask_main.py from a terminal. This will provide an address to enter into a web browser.
  - On the website, type your query into the textbox and press submit.
  - This will send you to another page that lists (up to) 10 subreddits we recommend based on your query.
 
## Team Member Contributions

-Kimberly and Miguel worked on using PRAW and pandas to scrape and index text data from various subreddits
-Ethan and Anthony worked on implementing the ranking algorithm using the mined subreddit post text data
-Nico worked on implementing the interface for the recommendation system based on the results from the ranking algorithm. 
