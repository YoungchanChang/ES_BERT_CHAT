from pathlib import Path
import platform

chat_log_path = Path(__file__).resolve().parent.parent.joinpath('chat_log')

chat_api_youtube = "chat_api_youtube"
chat_api_mrc = "chat_api_mrc"
mecab_ner = "mecab_ner"
chat_api_response = "chat_api_middleware"
entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner_app/data/entities/mecab_data"
intent_path = "/Users/youngchan/Desktop/ES_BERT_CHAT"
entity_path = "/Users/youngchan/Desktop/ES_BERT_CHAT"
bert_confirm = "mecab_bert_confirm"

if platform.system() == "Darwin":
    chat_api_mrc = "localhost"
    chat_api_youtube = "localhost"
    mecab_ner = "localhost"
    chat_api_response = "localhost"
    bert_confirm = "localhost"
    intent_path = "/user/local"
    entity_path = "/user/local"



youtube_response_url = f"http://{chat_api_youtube}:5210/chat_api_youtube/response_youtube"
mrc_response_url = f"http://{chat_api_mrc}:5220/chat_api_mrc/response_mrc"
mecab_ner = f"http://{mecab_ner}:5100/mecab_ner/mecab_attribute"
chat_api_response = f"http://{chat_api_response}:5200/chat_api/response_api"
bert_confirm_url = f"http://{bert_confirm}:5110/mecab_bert/bert_confirm"

intent_mecab_path = f"{intent_path}/mecab_ner_app/data/intents/mecab_data"
entity_mecab_path = f"{intent_path}/mecab_ner_app/data/entities/mecab_data"
