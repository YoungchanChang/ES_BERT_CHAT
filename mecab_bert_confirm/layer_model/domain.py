from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class MecabNerRequest(BaseModel):
    sentence: str
    all_category: str
    request_time: Optional[datetime] = datetime.now().isoformat(timespec='minutes')


class MecabNerResponse(BaseModel):
    bert_confirm: int
    response_time: Optional[datetime] = datetime.now().isoformat(timespec='minutes')
