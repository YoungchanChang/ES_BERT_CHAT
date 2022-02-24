import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv
from config.settings import mecab_ner, chat_api_response
from utility.custom_error import DockerNetworkException
from fastapi import FastAPI, HTTPException

TEMPLATE_DIR = Path(__file__).resolve().parent.parent.joinpath(".env")
load_dotenv(dotenv_path=str(TEMPLATE_DIR),verbose=True)


def get_mecab_ner_response(json_data):

    try:
        utility_answer = requests.post(
            mecab_ner, headers={'content-type': 'application/json'}, data=json_data
        )
        api_response = json.loads(utility_answer.text)
        return api_response

    except requests.ConnectionError as ce:
        # TODO sentry에 오류 메시지 전송
        print(ce)
    except Exception as e:
        print(e)


def get_chat_api_response(json_data):

    try:
        utility_answer = requests.post(
            chat_api_response, headers={'content-type': 'application/json'}, data=json_data
        )

        if utility_answer.status_code != 200:
            raise DockerNetworkException("chat_api_response")

        api_response = json.loads(utility_answer.text).get("api_response")
        return api_response

    except requests.ConnectionError as ce:
        # TODO sentry에 오류 메시지 전송
        print(ce)

    except Exception as e:
        raise


