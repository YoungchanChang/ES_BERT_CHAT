from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import List, Optional


class UserRequest(BaseModel):

    """ 사용자 요청 정보 """

    user_sentence: str
    user_ip: str
    user_request_time: Optional[datetime] = datetime.now().isoformat(timespec='microseconds')


class MecabNerAttribute(BaseModel):

    """ MecabNer 추출 정보 """

    category_sentence: str
    main_category: str
    entity: str
    entity_medium_category: str
    entity_small_category: str
    intent: str
    intent_medium_category: str
    intent_small_category: str
    bert_confirm: bool = False


class ChatApiRequest(BaseModel):

    """ ChatApi 서버에 보내는 요청 """

    user_info: UserRequest
    sentence_attributes: List[MecabNerAttribute]


class ChatApiResponse(BaseModel):

    """ ChatApi 서버에 보내는 응답 """

    api_response: str
    api_server: str


class TemplateRequestData(BaseModel):
    """ 템플릿에 요청 정보 """

    main_category: str
    entity_medium_category: str
    entity: str
    intent_small_category: str
