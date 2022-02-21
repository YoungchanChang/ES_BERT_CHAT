import os
import json
import requests


def get_bot_response(text_data):
    json_data = {
        "sentence": text_data
    }
    utility_answer = requests.post(
        os.getenv("bot_response"), headers={'content-type': 'application/json'}, data=json.dumps(json_data)
    )
    answer = json.loads(utility_answer.text).get("bot_response")
    return answer