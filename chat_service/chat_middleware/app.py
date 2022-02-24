import logging.config

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from layer_view import view

from config.settings import config_basic

logging.config.dictConfig(config_basic)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

app.include_router(view.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.exception_handler(Exception)
async def exception_general_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=418,
        content={"message": f"Nope wrong Ask"},
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="0.0.0.0", port=5001, reload=True
    )