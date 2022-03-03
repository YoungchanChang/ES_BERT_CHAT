from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import List, Optional


class TemplateItemRequest(BaseModel):

    entity_item_id: int
    intent_item_id: int
    template: str


class TemplateCategoryRequest(BaseModel):

    bind_category: str
    entity_category: str
    intent_category: str
    template: str

