from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import List, Optional


class Request(BaseModel):
    user_sentence: str
    user_request_time: datetime
    request_get_time: datetime = datetime.now().isoformat(timespec='microseconds')


class DjangoRequest(Request):
    ip_info: str


class ChatMiddlewareResponse(BaseModel):
    bot_response: str
    bot_response_time: datetime = datetime.now().isoformat(timespec='microseconds')


class MecabNerRequest(Request):
    ...


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


class MecabNerResponse(BaseModel):
    user_sentence: str
    is_atomic: bool
    sentence_attributes: List[MecabNerAttribute]
    system_response_time: datetime


class ChatApiRequest(MecabNerAttribute):
    request_time: datetime = datetime.now().isoformat(timespec='microseconds')


class ChatApiResponse(BaseModel):
    api_template: str
    api_server: str
    system_response_time: datetime
