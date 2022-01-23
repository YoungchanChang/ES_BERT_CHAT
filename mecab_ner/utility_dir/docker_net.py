import os
import json
import configparser
import requests

config = configparser.ConfigParser()
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURRENT_DIR)
config.read(CURRENT_DIR + "/config.ini")

bert_chat_container_url = config["server"]["bert_chat"]

headers = {'content-type': 'application/json'}


def get_entity_intent_answer(json_data):

    utility_answer = requests.post(
        bert_chat_container_url, headers=headers, data=json.dumps(json_data), timeout=3
    )

    answer = json.loads(utility_answer.text).get("answer")

    return answer
