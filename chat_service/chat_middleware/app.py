import logging.config

import uvicorn
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

from layer_view import view

from config.settings import config_basic

logging.config.dictConfig(config_basic)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

app.include_router(view.router)


@app.exception_handler(Exception)
async def exception_general_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=418,
        content={"message": f"Nope wrong Ask"},
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="0.0.0.0", port=5000, reload=True
    )