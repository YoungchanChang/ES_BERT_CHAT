import logging.config

import uvicorn
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from config.settings import config_basic
load_dotenv()

from layer_view import view


from utility.custom_error import TemplateNotExist

logging.config.dictConfig(config_basic)
logger = logging.getLogger(__name__)


app = FastAPI()

app.include_router(view.router)


@app.exception_handler(TemplateNotExist)
async def unicorn_exception_handler(request: Request, exc: TemplateNotExist):
    return JSONResponse(
        status_code=418,
        content={"message": f"Nope wrong Ask"},
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="0.0.0.0", port=5201, reload=True
    )