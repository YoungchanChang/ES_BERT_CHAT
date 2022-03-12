import os
import json
import requests
import logging
formatter = "%(asctime)s.%(msecs)03d\t%(levelname)s\t[%(name)s]\t%(message)s"
logging.basicConfig(level=logging.WARNING, format=formatter, datefmt='%m/%d/%Y %I:%M:%S')

def create_mecab_index(json_data):

    logging.WARNING({"mecab_create_index" : os.getenv("mecab_create_index")})

    utility_answer = requests.post(
        os.getenv("mecab_create_index"), headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
    )


    answer = json.loads(utility_answer.text).get("result")

    return answer


def insert_mecab_data(json_data):

    logging.WARNING({"mecab_insert_data": os.getenv("mecab_insert_data")})

    utility_answer = requests.post(
        os.getenv("mecab_insert_data"), headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
    )


    answer = json.loads(utility_answer.text).get("result")

    return answer

def insert_template_item(json_data):

    logging.WARNING({"insert_template_item": os.getenv("insert_template_item")})

    utility_answer = requests.post(
        os.getenv("insert_template_item"), headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
    )

    answer = json.loads(utility_answer.text).get("result")

    return answer

def insert_template_category(json_data):

    logging.WARNING({"insert_template_category": os.getenv("insert_template_category")})

    utility_answer = requests.post(
        os.getenv("insert_template_category"), headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
    )

    answer = json.loads(utility_answer.text).get("result")

    return answer