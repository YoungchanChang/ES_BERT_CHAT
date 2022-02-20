
import pytest
import json
from starlette.testclient import TestClient

from chat_middleware.app import app
from datetime import date

@pytest.fixture
def fastapi_client():
    return TestClient(app=app)


def test_request_from_django_web_well(fastapi_client, mock_django_request):

    with fastapi_client as client:
        result = client.post(f"chat_middleware/middleware_response", json=mock_django_request)

        assert result.status_code == 200


def test_request_from_django_web_wrong_time_format(fastapi_client, mock_django_request):

    mock_django_request["user_request_time"] = date(2002, 12, 4).isoformat()

    with fastapi_client as client:
        result = client.post(f"chat_middleware/middleware_response", json=mock_django_request)

        assert result.status_code == 422
