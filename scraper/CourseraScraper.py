import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CourseraScraper:
    def __init__(self, course_url: str, username: str, password: str) -> None:

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.url = course_url
        self.username = username
        self.password = password
        self.course_transcript_for_json = {}
        # Login to Coursera to allow scraper to parse pages
        CourseraScraperLogin(self.driver, self.username, self.password).login()
        self.driver.get(self.url)

    def run_scraper(self):
        # Parse course to get list of urls for each week to scrape
        course_transcripts = []

        course_parser = CourseraCourseParser(self.driver)
        course_name = course_parser.course_name

        # Parse each week url to get list of lecture URLs to scrape
        for week_url in course_parser.week_urls:
            week_str = "Week" + week_url.rsplit("/", 2)[-1]
            week_parser = CourseraWeekParser(self.driver, week_url)
            lecture_urls = week_parser.lecture_urls

            week_transcripts = []

            for lecture_url in lecture_urls:
                lecture_title = lecture_url.rsplit("/", 2)[-1]
                lecture_subtitles = week_parser.get_lecture_subtitles(lecture_url)
                week_transcripts.append({lecture_title: lecture_subtitles})

            course_transcripts.append({week_str: week_transcripts})

        self.course_transcript_for_json[course_name] = course_transcripts


class CourseraScraperLogin:
    def __init__(self, driver: webdriver.Chrome, email: str, password: str) -> None:
        self.driver = driver
        self.url = "https://www.coursera.org"
        self.login_email = email
        self.login_password = password

    def login(self) -> None:
        login_url = self.url + "/?authMode=login"
        self.driver.get(login_url)
        self.driver.find_element("id", "email").send_keys(self.login_email)
        self.driver.find_element("id", "password").send_keys(self.login_password)
        self.driver.find_element("xpath", "//button[@type='submit']").click()
        input("Finalize CAPTCHA and then press Enter in the shell")



class CourseraCourseParser:
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.course_name = self.parse_course_name()
        self.get_week_urls()

    def parse_course_name(self) -> str:
        # TODO: Automatically parse course name
        return "TODO"

    def get_week_urls(self) -> None:
        """Initialize the URLs for each week of the course"""
        self.landing_page = self.driver.current_url
        # Coursera defaults to saving the user's last accessed week, so need to get the true landing
        # page once it's been navigated to
        self.landing_page = self.landing_page.split('week')[0]

        week_url_list = []
        if "https://www.coursera.org/learn/" in self.landing_page:
            self.driver.get(self.landing_page)
            week_list_xpath_pattern = "//*[@class='cds-108 css-1mxkpit cds-110']"
            # Need to make sure the element loads on the page before it can be scraped
            try:
                myElem = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, week_list_xpath_pattern)))
            except TimeoutException:
                print("Loading took too much time!")
            # Get all elements from the sidebare containing links to the course's week lectures
            week_elements = self.driver.find_elements(
                By.XPATH,
                week_list_xpath_pattern)

            for week_number in range(1, len(week_elements)+1):
                week_url_list.append(self.landing_page + f"week/{week_number}")
        else:
            self.get_week_urls()

        self.week_urls = week_url_list


class CourseraWeekParser:
    def __init__(self, driver: webdriver.Chrome, week_url: str) -> None:
        self.driver = driver
        self.week_url = week_url
        self.get_lecture_urls()

    def get_lecture_urls(self):
        lecture_urls = []
        soup = self.get_page_soup(self.week_url)
        elements = soup.find_all("div", attrs={"data-test": "WeekSingleItemDisplay-lecture"})

        for element in elements:
            a_tag = element.find('a')
            if a_tag and 'href' in a_tag.attrs:
                href_value = a_tag['href']
                lecture_urls.append("https://www.coursera.org" + href_value)
            else:
                print("href attribute not found")
        self.lecture_urls = lecture_urls

    def get_lecture_subtitles(self, lecture_url):
        soup = self.get_page_soup(lecture_url)
        subtitles = []

        # Find all div elements contain subtitles
        # TODO: Take another look at this and see if XPATH is more accurate. Looks like this pattern isn't consistent across classes
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

        # Process the subtitles
        return subtitles

    def get_page_soup(self, url: str) -> BeautifulSoup:
        # Take driver to specified URL
        self.driver.get(url)
        # Insert a sleep timer to avoid being flagged as a bot
        # TODO: Replace this with a wait call to make sure the required element loads correctly
        time.sleep(4)

        # get the page source and parse the HTML content into a BeautifulSoup object
        parge_source = self.driver.page_source
        soup = BeautifulSoup(parge_source, 'html.parser')

        return soup
