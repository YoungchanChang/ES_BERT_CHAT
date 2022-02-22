import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from chat_service.chat_api_service.chat_api_youtube.layer_view import view

load_dotenv()

app = FastAPI()

app.include_router(view.router)

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="0.0.0.0", port=5210, reload=True
    )