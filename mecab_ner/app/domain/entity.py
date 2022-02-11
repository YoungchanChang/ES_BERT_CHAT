from dataclasses import dataclass
from typing import Optional


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

