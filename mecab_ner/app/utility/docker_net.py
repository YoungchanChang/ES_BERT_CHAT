import os
import json
import requests


def get_entity_intent_answer(json_data):

    utility_answer = requests.post(
        os.getenv("bert_chat"), headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
    )

    answer = json.loads(utility_answer.text).get("answer")

    return answer
