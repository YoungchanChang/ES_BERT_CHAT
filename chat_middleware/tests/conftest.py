import pytest


@pytest.fixture(scope="function")
def mock_django_request():
    return {
        "user_sentence": "핼로 월드",
        "user_request_time": "2022-02-21T07:03:52.716025",
        "ip_info" : "127.0.0.1"
    }