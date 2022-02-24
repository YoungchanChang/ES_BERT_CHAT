from chat_core.settings import *
from chat_core.chat_log_config import config_basic

config_basic['handlers']['access']['filename'] = str(chat_log_path.joinpath('chat_api_youtube', 'access', 'access.log'))
config_basic['handlers']['warning']['filename'] = str(chat_log_path.joinpath('chat_api_youtube', 'warning', 'warning.log'))
config_basic['handlers']['error']['filename'] = str(chat_log_path.joinpath('chat_api_youtube', 'error', 'error.log'))
config_basic['handlers']['critical']['filename'] = str(chat_log_path.joinpath('chat_api_youtube', 'critical', 'critical.log'))
