import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

driver = webdriver.Firefox()
coursera_url = "https://www.coursera.org"
# ---------------------------------------------------------

def get_soup(url):
    driver.get(url)
    time.sleep(20)

    # Get the page source and parse the HTML content
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup

def login():
    # Open the login page
    login_url = coursera_url + "/?authMode=login"
    driver.get(login_url)

    # Ensure the page has loaded
    input("Login and navigate to the course page, then press 'Enter' here")

def get_week_urls():

    # current_url = driver.current_url
    # print("Current" + current_url) # To Be Done
    current_url = "https://www.coursera.org/learn/text-mining/home/week/1"

    if "https://www.coursera.org/learn/" in current_url:
        week_urls = []

        soup = get_soup(current_url)
        # Count number of weeks this course has
        # num_weeks = len(soup.find_all()) # To Be Done


        for i in range(6):
            week_url = current_url[:-1] + str(i + 1)
            week_urls.append(week_url)
        print(week_urls)
        return week_urls
    else:
        input("Navigate to the right page, then press 'Enter'.")
        get_week_urls()

def get_lecture_urls(week_url):
    lecture_urls = []
    soup = get_soup(week_url)

    elements = soup.find_all("div", attrs={"data-test":"WeekSingleItemDisplay-lecture"})
    for element in elements:
        a_tag = element.find('a')
        if a_tag and 'href' in a_tag.attrs:
            href_value = a_tag['href']
            lecture_urls.append(coursera_url + href_value)
        else:
            print("href attribute not found")
    print(lecture_urls)
    return lecture_urls

def get_lecture_subtitles(lecture_url):

    soup = get_soup(lecture_url)
    subtitles = []

    # Find all div elements contain subtitles
    pattern = re.compile(r'\bcss-1shylkf\b')
    elements = soup.find_all('div', class_=pattern)
    if len(elements) == 0:
        print("No value retrieved")
    else:
        print("Retrieved")

    for element in elements:
        # Extract the timestamp
        button = element.find('button', class_='timestamp')
        timestamp = button.contents[-1].strip()

        # Extract all phrase elements and concatenate the text of all subtitles
        phrases = element.find_all('div', class_='phrases')
        text_content = ' '.join(phrase.get_text().strip() for phrase in phrases)

        # Append the subtitles to the list as a dictionary
        subtitles.append({'time': timestamp, 'text': text_content, 'url': lecture_url})

    # Print or process the subtitles
    # print(subtitles)
    return subtitles

# ---------------------------------------------------------

# Set up options
options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')  # This may be necessary in a headless environment
options.add_argument('--disk-cache-dir=/Users/jnfng_w/Documents/Cofig')
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)


login()

# Get course name # To Be Done
course_name = "Text Mining and Analytics"
week_urls = get_week_urls()
subtitles_of_course = []
for week_url in week_urls:

    # Which week
    week = "Week " + week_url.rsplit("/", 2)[-1]
    lecture_urls = get_lecture_urls(week_url)
    subtitles_of_week = []
    for lecture_url in lecture_urls:

        # Get course title
        course_title = lecture_url.rsplit("/",2)[-1]
        lecture_subtitles = get_lecture_subtitles(lecture_url)
        subtitles_of_week.append({course_title: lecture_subtitles})
    subtitles_of_course.append({week: subtitles_of_week})
subtitle_package = {course_name: subtitles_of_course}

# Writing a JSON file
with open('subtitles.json', 'w') as json_file:
    json.dump(subtitle_package, json_file, indent=4)


