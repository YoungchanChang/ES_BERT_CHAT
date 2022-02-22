from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import List, Optional


class Request(BaseModel):

    """ 사용자 요청 정보 """

    user_sentence: str
    user_ip: str
    user_request_time: datetime
    request_get_time: datetime = datetime.now().isoformat(timespec='microseconds')


class Response(BaseModel):

    """ 시스템 응답 정보 """

    system_response_time: datetime = datetime.now().isoformat(timespec='microseconds')


class MecabNerAttribute(BaseModel):
    category_sentence: str
    main_category: str
    entity: str
    entity_medium_category: str
    entity_small_category: str
    intent: str
    intent_medium_category: str
    intent_small_category: str
    bert_confirm: bool


class TemplateRequestData(BaseModel):
    main_category: str
    entity_medium_category: str
    entity: str
    intent_small_category: str


class ChatApiRequest(BaseModel):

    """ ChatApi 서버에 보내는 요청 """

    req: Request
    sentence_attributes: List[MecabNerAttribute]


class ChatApiResponse(Response):

    """ ChatApi 서버에 보내는 응답 """

    api_response: str
    api_server: str
