import logging.config
from pathlib import Path

from chat_core import chat_decorator

from config.settings import config_basic

logging.config.dictConfig(config_basic)
logger = logging.getLogger('decorator')


file_path = str(Path(__file__).resolve().relative_to(Path(__file__).cwd()))


@chat_decorator.log_basic(logger=logger, path=file_path)
def get_mrc(sentence_attributes: str):
    return "잘 모르겠어요. 제가 공부해서 꼭 알려드릴께요!"
