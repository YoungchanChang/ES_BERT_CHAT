import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv

from app.utility.custom_error import BertConfirmException

load_dotenv()


def get_bert_confirm_response(json_data):

    try:
        utility_answer = requests.post(
            os.getenv("bert_confirm_response"), headers={'content-type': 'application/json'}, data=json_data
        )
        if utility_answer.status_code == 200:
            bert_confirm_response = json.loads(utility_answer.text).get("bert_confirm")
            return bert_confirm_response
        raise BertConfirmException
    except requests.ConnectionError as ce:
        # TODO sentry에 오류 메시지 전송
        print(ce)
    except Exception as e:
        print(e)
