import json

import requests
import sys, os
from datetime import datetime
from elasticsearch import Elasticsearch

ES_URL = os.environ.get("ES_URL", "https://cs410-project.es.us-central1.gcp.cloud.es.io")
ES_USER = os.environ.get("ES_USER", "elastic")
#ES_PASSWORD = os.environ.get("ES_PASSWORD", "CS410-project") ##"pciWclpLNdXuicUhXV8bhgk2")
ES_PASSWORD = os.environ.get("ES_PASSWORD", "pciWclpLNdXuicUhXV8bhgk2")



def write_to_es(doc):
    es = Elasticsearch(ES_URL,
                       http_auth=(ES_USER, ES_PASSWORD)
    )
    resp = es.index(index="subtitles", document=doc)
    print(resp['result'])

def index_subtitles():
    with open('./subtitles.json') as f:
        subtitles_doc = f.read()
        subtitles_json = json.loads(subtitles_doc)
        for weeks in subtitles_json['Text Mining and Analytics']:
            for week in weeks.values():
                for lecture_titles in week:
                    for lecture_title in lecture_titles:
                        for subtitles in lecture_titles[lecture_title]:
                            write_to_es(subtitles)


if __name__ == '__main__':
    index_subtitles()