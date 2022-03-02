from pathlib import Path
from typing import List

import numpy as np

from app.controller.service.mecab_binder import MecabBinder
from chat_service.chat_core.chat_domain import MecabFeature, MecabSimpleFeature, MecabBertBindFeature

INTENT_POSSIBLE_CATEGORY = []


def get_mecab_bind_feature(sentence):

    m_b = MecabBinder()
    bind_result = m_b.get_bind(sentence)

    bind_result.bind_list = m_b.split_multi_en_in(sentence, bind_result.bind_list)

    m_b_d_list = [MecabBertBindFeature(bind_category=x.bind_category, bind_sentence=x.bind_sentence,
                                       entity=MecabFeature(value=x.entity.word,
                                                           large_category=x.entity.category.large,
                                                           small_category=x.entity.category.small),
                                       intent=MecabFeature(value=x.intent.word,
                                                           large_category=x.intent.category.large,
                                                           small_category=x.intent.category.small),
                                       ) for x in bind_result.bind_list]
    entity_list = [MecabSimpleFeature(user_sentence=sentence, value=x.word, large_category=x.category.large,
                                small_category=x.category.small) for x in bind_result.entity_list]
    intent_list = [MecabSimpleFeature(user_sentence=sentence, value=x.word, large_category=x.category.large,
                                      small_category=x.category.small) for x in bind_result.intent_list if
                   x.category.large in INTENT_POSSIBLE_CATEGORY]
    return m_b_d_list, entity_list, intent_list

if __name__ == "__main__":
    sentence = "치킨이랑 진주 아이유 듣는 것이 좋다 아이묭 좋아해 동대문 좋아"
    value = get_mecab_bind_feature(sentence)
    a = 3