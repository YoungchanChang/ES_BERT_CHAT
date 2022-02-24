import logging.config

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from layer_view import view

from config.settings import config_basic

logging.config.dictConfig(config_basic)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

app.include_router(view.router)

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="0.0.0.0", port=5220, reload=True
    )