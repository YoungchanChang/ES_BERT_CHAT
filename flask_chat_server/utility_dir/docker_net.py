import os
import json
import configparser
import requests

config = configparser.ConfigParser()
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURRENT_DIR)
config.read(CURRENT_DIR + "/config.ini")

headers = {'content-type': 'application/json'}
mecab_ner_container_url = config["server"]["mecab_ner"]


def get_mecab_ner_answer(query):
    json_data = {
        "query" : query
    }
    utility_answer = requests.post(
        mecab_ner_container_url, headers=headers, data=json.dumps(json_data)
    )

    answer = json.loads(utility_answer.text).get("answer")

    return answer
