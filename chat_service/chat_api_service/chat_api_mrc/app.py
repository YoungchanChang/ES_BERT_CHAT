import logging.config

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from layer_view import view

from chat_core.chat_log_config import config_basic
from chat_core.settings import chat_log_path

config_basic['handlers']['access']['filename'] = str(chat_log_path.joinpath('chat_api_mrc', 'access', 'access.log'))
config_basic['handlers']['error']['filename'] = str(chat_log_path.joinpath('chat_api_mrc', 'error', 'error.log'))
logging.config.dictConfig(config_basic)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

app.include_router(view.router)

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="0.0.0.0", port=5220, reload=True
    )