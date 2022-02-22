import os
import json
from datetime import datetime

import requests


def get_bot_response(text_data):
    json_data = {
        "user_sentence": text_data,
        "user_ip" : "127.0.0.1",
        "user_request_time": datetime.now().isoformat(timespec='microseconds')
    }
    utility_answer = requests.post(
        os.getenv("bot_response"), headers={'content-type': 'application/json'}, data=json.dumps(json_data)
    )
    answer = json.loads(utility_answer.text).get("bot_response")
    return answer