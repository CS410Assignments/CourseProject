import json
import os
from elasticsearch import Elasticsearch


class ElasticSearchJSONWriter:
    """
    Class to take a JSON script and write it to ElasticSearch, so it can be used in the Coursera
    search extension.
    The current implementation uses the project team's ElasticSearch instance, but this can be
    changed by modifying the 'ES_URL' default value in the class __init__() method below.
    """

    def __init__(self, json_path: str = "./subtitles.json"):
        self.url = os.environ.get(
            "ES_URL", "https://ac55987c83844faa90726d4e5efe92b9.us-central1.gcp.cloud.es.io"
        )
        self.user = os.environ.get("ES_USER", "elastic")
        self.password = os.environ.get("ES_PASSWORD", "pciWclpLNdXuicUhXV8bhgk2")
        self.json_path = json_path
        self.subtitles_json = self.load_json()

    def load_json(self) -> json:
        """Load JSON file from saved scraped results in preparation to be pusehd to ElasticSearch"""
        try:
            with open(self.json_path) as f:
                subtitles_doc = f.read()
                subtitles_json = json.loads(subtitles_doc)
        # Should always work unless the file doesn't exist, in which case the user should be warned
        except FileNotFoundError:
            print(f"{self.json_path} was not found")

        return subtitles_json

    def index_subtitles(self, course_name: str) -> None:
        for weeks in self.subtitles_json[course_name]:
            week_val = list(weeks.keys())[0]
            for week in weeks.values():
                for lecture_titles in week:
                    for lecture_title in lecture_titles:
                        for subtitles in lecture_titles[lecture_title]:
                            subtitles["lecture_title"] = lecture_title
                            subtitles["week"] = week_val
                            subtitles['course_name'] = course_name
                            self.write_to_elasticsearch(subtitles)
        print(f"Successfully indexed subtitles for {course_name}")

    def write_to_elasticsearch(self, doc) -> None:
        es = Elasticsearch(self.url, http_auth=(self.user, self.password))
        resp = es.index(index="subtitles", document=doc)
        print(resp["result"])
