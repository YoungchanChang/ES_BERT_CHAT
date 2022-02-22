from typing import List

from chat_service.chat_api_youtube.layer_model.domain import MecabNerAttribute
from chat_service.chat_api_youtube.utility.custom_error import NoMusicData

FIRST_VALUE = 0

temp_dict = {
    "아이유": "https://www.youtube.com/watch?v=3iM_06QeZi8",
    "아이유 블루밍": "https://www.youtube.com/watch?v=yqtCGojXEpM",
}


def get_youtube_music(sentence_attributes: List[MecabNerAttribute]):

    youtube_music_entity = [x.entity for x in sentence_attributes]

    youtube_link = " ".join(youtube_music_entity)
    youtube_data = temp_dict.get(youtube_link, None)

    if youtube_data:
        return youtube_data

    raise NoMusicData
