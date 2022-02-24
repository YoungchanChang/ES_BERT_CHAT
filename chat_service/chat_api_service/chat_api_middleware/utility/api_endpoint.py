import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv

TEMPLATE_DIR = Path(__file__).resolve().parent.parent.joinpath(".env")
load_dotenv(dotenv_path=str(TEMPLATE_DIR),verbose=True)
from config.settings import youtube_response_url, mrc_response_url

def get_youtube_api_response(json_data):

    try:
        utility_answer = requests.post(
            youtube_response_url, headers={'content-type': 'application/json'}, data=json_data
        )
        api_response = json.loads(utility_answer.text).get("api_response")
        return api_response

    except requests.ConnectionError as ce:
        # TODO sentry에 오류 메시지 전송
        print(ce)
    except Exception as e:
        print(e)


def get_mrc_api_response(json_data):

    try:
        utility_answer = requests.post(
            mrc_response_url, headers={'content-type': 'application/json'}, data=json.dumps(json_data), timeout=3
        )
        api_response = json.loads(utility_answer.text).get("api_response")
        return api_response

    except requests.ConnectionError as ce:
        # TODO sentry에 오류 메시지 전송
        print(ce)
    except Exception as e:
        print(e)
