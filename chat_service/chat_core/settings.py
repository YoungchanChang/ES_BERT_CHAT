from pathlib import Path
import platform

chat_log_path = Path(__file__).resolve().parent.parent.joinpath('chat_log')

chat_api_youtube = "chat_api_youtube"
chat_api_mrc = "chat_api_mrc"
mecab_ner = "mecab_ner"
chat_api_response = "chat_api_middleware"
if platform.system() == "Darwin":
    chat_api_mrc = "localhost"
    chat_api_youtube = "localhost"
    mecab_ner = "localhost"
    chat_api_response = "localhost"


youtube_response_url = f"http://{chat_api_youtube}:5210/chat_api_youtube/response_youtube"
mrc_response_url = f"http://{chat_api_mrc}:5220/chat_api_mrc/response_mrc"
mecab_ner = f"http://{mecab_ner}:5100/mecab_ner/mecab_attribute"
chat_api_response = f"http://{chat_api_response}:5200/chat_api/response_api"