import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from chat_middleware.layer_view import view

load_dotenv()

app = FastAPI()

app.include_router(view.router)

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="0.0.0.0", port=5000, reload=True
    )