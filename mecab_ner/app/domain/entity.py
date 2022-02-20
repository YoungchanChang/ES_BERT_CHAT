from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel

@dataclass
class MecabDomain:
    ...


@dataclass
class MecabWordFeature(MecabDomain):
    word: str
    pos: str
    semantic: str
    has_jongseong: bool
    reading: str
    type : str
    start_pos: str
    end_pos: str
    expression: str
    space_token_idx: Optional[int] = None
    mecab_token_idx: Optional[int] = None


@dataclass
class MecabCategory(MecabDomain):
    large_category: str
    medium_category: str
    small_category: str
    start_idx: Optional[int] = None
    end_idx: Optional[int] = None
    entity: Optional[str] = None


@dataclass
class MeCabEntityIntent(MecabDomain):
    entity: MecabCategory
    intent: MecabCategory


@dataclass
class MeCabEntity(MecabDomain):
    entity: MecabCategory


@dataclass
class MeCabIntent(MecabDomain):
    intent: MecabCategory


class Query(BaseModel):
    sentence: str


class CategoryItem(BaseModel):
    large_category: str
    medium_category: str
    small_category: str
    type: str

class MecabWord(BaseModel):
    word: str
    category: int
    type: str