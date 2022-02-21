import os
import json
from datetime import date
from dotenv import load_dotenv
import requests_mock
load_dotenv()

def test_request_from_django_web_well(fastapi_client, mock_django_request):

    with fastapi_client as client:
        result = client.post(f"chat_middleware/middleware_response", json=mock_django_request)

        assert result.status_code == 200


def test_request_from_django_web_wrong_time_format(fastapi_client, mock_django_request):

    mock_django_request["user_request_time"] = date(2002, 12, 4).isoformat()

    with fastapi_client as client:
        result = client.post(f"chat_middleware/middleware_response", json=mock_django_request)

        assert result.status_code == 422


def test_mecab_ner(requests_mock, mock_mecab_ner_response):
    # ref : https://stackoverflow.com/questions/63957899/requests-mock-how-can-i-match-posted-payload-in-a-mocked-endpoint
    mecab_ner_response = json.loads(mock_mecab_ner_response.json())

    requests_mock.get(os.getenv("mecab_ner_info"), json=mecab_ner_response)

