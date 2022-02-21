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


class ChatMiddlewareResponse(Response):
    """ 챗미들웨어 서버에서 보내는 응답 """

    bot_response: str


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


class MecabNerResponse(Response):

    """ MecabNer에서 받는 응답 """

    user_sentence: str
    is_atomic: bool
    sentence_attributes: List[MecabNerAttribute]


class ChatApiRequest(BaseModel):

    """ ChatApi 서버에 보내는 요청 """

    req: Request
    is_atomic: bool
    sentence_attributes: List[MecabNerAttribute]


class ChatApiResponse(Response):

    """ ChatApi 서버에 보내는 응답 """

    api_response: str
    api_server: str
