from pathlib import Path
import platform

chat_log_path = Path(__file__).resolve().parent.parent.joinpath('chat_log')

chat_api_youtube = "chat_api_youtube"
chat_api_mrc = "chat_api_mrc"
if platform.system() == "Darwin":
    chat_api_mrc = "localhost"
    chat_api_youtube = "localhost"


youtube_response_url = f"http://{chat_api_youtube}:5210/chat_api_youtube/response_youtube"
mrc_response_url = f"http://{chat_api_mrc}:5220/chat_api_mrc/response_mrc"
