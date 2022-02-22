import pytest
from starlette.testclient import TestClient

from chat_service.chat_middleware.app import app
from chat_service.chat_middleware.layer_model.domain import MecabNerAttribute, MecabNerResponse, ChatApiRequest, ChatApiResponse, \
    Request


@pytest.fixture(scope="function")
def mock_django_request():
    return {
        "user_sentence": "핼로 월드",
        "user_request_time": "2022-02-21T07:03:52.716025",
        "user_ip" : "127.0.0.1"
    }


@pytest.fixture
def fastapi_client():
    return TestClient(app=app)


@pytest.fixture(scope="function")
def mock_mecab_ner_response():
    m_n_attr = MecabNerAttribute(category_sentence="나는 후라이드 치킨이 좋아", main_category="food",
                      entity="후라이드 치킨", entity_medium_category="fastfood", entity_small_category="패스트 푸드",
                      intent="좋", intent_medium_category="like", intent_small_category="좋다",
                      bert_confirm=True)
    m_n_res = MecabNerResponse(user_sentence="나는 후라이드 치킨이 좋아", is_atomic=True, system_response_time="2022-02-21T07:03:52.716025",
                     sentence_attributes=[m_n_attr])

    return m_n_res


@pytest.fixture(scope="function")
def mock_chat_api_request():
    m_n_attr = MecabNerAttribute(category_sentence="나는 후라이드 치킨이 좋아", main_category="food",
                      entity="후라이드 치킨", entity_medium_category="fastfood", entity_small_category="패스트 푸드",
                      intent="좋", intent_medium_category="like", intent_small_category="좋다",
                      bert_confirm=True)
    req = Request(user_sentence="나는 후라이드 치킨이 좋아",user_request_time="2022-02-21T07:03:52.716025",
                   user_ip="127.0.0.1")

    c_a_req = ChatApiRequest(m_n_attr=m_n_attr, req=req)


    return c_a_req


@pytest.fixture(scope="function")
def mock_chat_api_response():
    c_a_res = ChatApiResponse(api_template="나도 치킨이 좋아요", api_server="basic_template", system_response_time="2022-02-21T07:03:52.716025")

    return c_a_res

