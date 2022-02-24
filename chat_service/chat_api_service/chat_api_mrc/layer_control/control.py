import logging
from typing import List
from pathlib import Path

from chat_service.chat_core import log_decorator
from chat_core.chat_domain import MecabNerAttribute

logger = logging.getLogger('decorator')

file_path = str(Path(__file__).resolve().relative_to(Path(__file__).cwd()))


@log_decorator.log_basic(logger=logger, path=file_path)
def get_mrc(sentence_attributes: List[MecabNerAttribute]):
    return "잘 모르겠어요. 제가 공부해서 꼭 알려드릴께요!"
