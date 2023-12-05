import json
import os
from elasticsearch import Elasticsearch


class ElasticSearchJSONWriter:
    def __init__(self, json_path: str = "./subtitles.json"):
        self.url = os.environ.get(
            "ES_URL", "https://search-cs410-project-hw5dhpc4jsg3m74vnbalajt754.aos.us-east-1.on.aws"
        )
        self.user = os.environ.get("ES_USER", "elastic")
        self.password = os.environ.get("ES_PASSWORD", "CS410-project")
        self.json_path = json_path
        self.subtitles_json = self.load_json(self.json_path)

    def load_json(self) -> json:
        try:
            with open(self.json_path) as f:
                subtitles_doc = f.read()
                subtitles_json = json.loads(subtitles_doc)
        except FileNotFoundError as e:
            print(f"{self.json_path} was not found")

        return subtitles_json

    def index_subtitles(self) -> None:
        for weeks in self.subtitles_json["Text Mining and Analytics"]:
            for week in weeks.values():
                for lecture_titles in week:
                    for lecture_title in lecture_titles:
                        for subtitles in lecture_titles[lecture_title]:
                            self.write_to_elasticsearch(subtitles)

    def write_to_elasticsearch(self, doc) -> None:
        es = Elasticsearch(self.url, http_auth=(self.user, self.password))
        resp = es.index(index="subtitles", document=doc)
        print(resp["result"])
