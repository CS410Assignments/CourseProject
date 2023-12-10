import argparse
import json

from CourseraScraper import CourseraScraper
from ElasticSearchJSONWriter import ElasticSearchJSONWriter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--course_url",
        required=True,
        type=str,
        help="URL to the landing page of the course you want to scrape. Ex: https://www.coursera.org/learn/cs-410/home/",
    )
    parser.add_argument("-u", "--username", required=True, type=str, help="Coursera Username")
    parser.add_argument("-p", "--password", required=True, type=str, help="Coursera Password")
    parser.add_argument("-e", "--elastic_search_push", action="store_true")
    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        default="./subtitles.json",
        help="Path to write JSON file containing scraped transcripts to",
    )
    args = parser.parse_args()

    # Scrape a Coursera course's transcripts into a JSON file
    scraper = CourseraScraper(args.course_url, args.username, args.password)
    scraper.run_scraper()

    # Writing a JSON file
    with open(args.output_path, "w") as json_file:
        json.dump(scraper.course_transcript_for_json, json_file, indent=4)
    if args.elastic_search_push:
        writer = ElasticSearchJSONWriter(args.output_path)
        writer.index_subtitles()
