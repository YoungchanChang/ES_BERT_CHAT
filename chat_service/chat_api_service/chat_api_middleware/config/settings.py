from chat_core.settings import *
from chat_core.chat_log_config import config_basic

service_name = 'chat_api_middleware'

config_basic['handlers']['access']['filename'] = str(chat_log_path.joinpath(service_name, 'access', 'access.log'))
config_basic['handlers']['warning']['filename'] = str(chat_log_path.joinpath(service_name, 'warning', 'warning.log'))
config_basic['handlers']['error']['filename'] = str(chat_log_path.joinpath(service_name, 'error', 'error.log'))
config_basic['handlers']['critical']['filename'] = str(chat_log_path.joinpath(service_name, 'critical', 'critical.log'))
