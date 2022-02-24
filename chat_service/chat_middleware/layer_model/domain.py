from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import List, Optional


class SimpleRequest(BaseModel):
    """ 사용자 요청 정보 """

    user_sentence: str
    user_request_time: datetime = datetime.now().isoformat(timespec='microseconds')


class BotResponse(BaseModel):

    """ ChatApi 서버에 보내는 응답 """

    bot_response: str
    bot_response_time: datetime = datetime.now().isoformat(timespec='microseconds')
