import os
import json
import requests


def create_mecab_index(json_data):

    utility_answer = requests.post(
        os.getenv("mecab_create_index"), headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
    )

    answer = json.loads(utility_answer.text).get("answer")

    return answer


def insert_mecab_data(json_data):

    utility_answer = requests.post(
        os.getenv("mecab_insert_data"), headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
    )

    answer = json.loads(utility_answer.text).get("answer")

    return answer

def insert_template_item(json_data):

    utility_answer = requests.post(
        os.getenv("insert_template_item"), headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
    )

    answer = json.loads(utility_answer.text).get("result")

    return answer

def insert_template_category(json_data):

    utility_answer = requests.post(
        os.getenv("insert_template_category"), headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
    )

    answer = json.loads(utility_answer.text).get("result")

    return answer