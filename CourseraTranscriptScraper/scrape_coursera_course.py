import argparse
import json
from CourseraScraper import CourseraScraper
from ElasticSearchJSONWriter import ElasticSearchJSONWriter


def scrape_course_pipeline(
    course_url: str, username: str, password: str, elastic_search_push: bool
) -> None:
    # Scrape a Coursera course's transcripts into a JSON file
    scraper = CourseraScraper(course_url, username, password)
    scraper.run_scraper()
    # Generate the JSON filename to write subtitles to from the course name
    course_name = scraper.course_name
    course_code = course_name.split(":")[0].replace(' ', '')
    output_path = f"subtitles_{course_code}.json"

    # Writing a JSON file
    with open(output_path, "w") as json_file:
        json.dump(scraper.course_transcript_for_json, json_file, indent=4)
    if elastic_search_push:
        writer = ElasticSearchJSONWriter(output_path)
        writer.index_subtitles(course_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--course_url",
        required=True,
        type=str,
        help="URL to the landing page of the course you want to scrape. \
            Ex: https://www.coursera.org/learn/cs-410/home/",
    )
    parser.add_argument("-u", "--username", required=True, type=str, help="Coursera Username")
    parser.add_argument("-p", "--password", required=True, type=str, help="Coursera Password")
    parser.add_argument("-e", "--elastic_search_push", action="store_true")
    args = parser.parse_args()

    scrape_course_pipeline(args.course_url, args.username, args.password, args.elastic_search_push)
