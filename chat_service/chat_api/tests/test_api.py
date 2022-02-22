import os
import json
from dotenv import load_dotenv
import requests_mock

load_dotenv()


def test_request_chat_middleware(fastapi_client, mock_chat_middleware_request):

    with fastapi_client as client:
        result = client.post(f"chat_middleware/middleware_response", json=mock_chat_middleware_request)

        assert result.status_code == 200


def test_chat_youtube_response(requests_mock, mock_chat_api_response):
    chat_api_response = json.loads(mock_chat_api_response.json())

    requests_mock.get(os.getenv("youtube_response"), json=chat_api_response)


def test_chat_mrc_response(requests_mock, mock_chat_api_response):
    chat_api_response = json.loads(mock_chat_api_response.json())

    requests_mock.get(os.getenv("youtube_response"), json=chat_api_response)