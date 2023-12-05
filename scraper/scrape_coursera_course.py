import argparse
import json

from CourseraScraper import CourseraScraper

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--course_url", required=True, type=str, help="URL to the landing page of the course you want to scrape. Ex: https://www.coursera.org/learn/cs-410/home/")
    parser.add_argument('-u', "--username", required=True, type=str, help="Coursera Username")
    parser.add_argument('-p', "--password", required=True, type=str, help="Coursera Password")
    args = parser.parse_args()

    scraper = CourseraScraper(args.course_url, args.username, args.password)
    scraper.run_scraper()
    print(scraper.course_transcript_for_json)

    # Writing a JSON file
    with open('subtitles.json', 'w') as json_file:
        json.dump(scraper.course_transcript_for_json, json_file, indent=4)
