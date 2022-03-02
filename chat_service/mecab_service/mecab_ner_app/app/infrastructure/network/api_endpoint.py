import os
import json
from pathlib import Path

import requests
from dotenv import load_dotenv

from app.domain.mecab_exception import BertConfirmException
from chat_service.chat_core.settings import bert_confirm_url

load_dotenv()


def get_bert_confirm_response(json_data):

    try:
        utility_answer = requests.post(
            bert_confirm_url, headers={'content-type': 'application/json'}, data=json_data
        )
        if utility_answer.status_code == 200:
            bert_confirm_response = json.loads(utility_answer.text)
            return bert_confirm_response
        raise BertConfirmException

    except requests.ConnectionError as ce:
        # TODO sentry에 오류 메시지 전송
        print(ce)
    except Exception as e:
        print(e)
