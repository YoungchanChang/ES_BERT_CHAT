import logging.config

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from chat_service.chat_api_service.chat_api_youtube.layer_view import view

from chat_core.chat_log_config import config_basic
from chat_core.settings import chat_log_path


config_basic['handlers']['access']['filename'] = str(chat_log_path.joinpath('chat_api_youtube', 'access', 'access.log'))
config_basic['handlers']['warning']['filename'] = str(chat_log_path.joinpath('chat_api_youtube', 'warning', 'warning.log'))
config_basic['handlers']['error']['filename'] = str(chat_log_path.joinpath('chat_api_youtube', 'error', 'error.log'))
logging.config.dictConfig(config_basic)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

app.include_router(view.router)

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="0.0.0.0", port=5210, reload=True
    )