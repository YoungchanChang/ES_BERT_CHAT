import os
import json
import requests


def get_mecab_ner(text_data):
    json_data = {
        "sentence": text_data
    }
    utility_answer = requests.post(
        os.getenv("mecab_ner"), headers={'content-type': 'application/json'}, data=json.dumps(json_data)
    )
    answer = json.loads(utility_answer.text).get("answer")
    return answer