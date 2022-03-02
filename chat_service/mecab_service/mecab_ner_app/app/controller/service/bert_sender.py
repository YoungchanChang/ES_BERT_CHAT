from pathlib import Path
from typing import List

import numpy as np

from app.controller.service.mecab_binder import MecabBinder
from app.chat_core.chat_domain import MecabFeature, MecabSimpleFeature, MecabBertBindFeature


def get_mecab_bind_feature(sentence: str, mecab_binder: MecabBinder = None, intent_category: List = None):

    if mecab_binder is None:
        mecab_binder = MecabBinder()

    if intent_category is None:
        intent_category = []

    bind_result = mecab_binder.get_bind(sentence)

    bind_result.bind_list = mecab_binder.split_multi_en_in(sentence, bind_result.bind_list)

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
                   x.category.large in intent_category]
    return m_b_d_list, entity_list, intent_list

if __name__ == "__main__":
    sentence = "치킨이랑 진주 아이유 듣는 것이 좋다 아이묭 좋아해 동대문 좋아"
    value = get_mecab_bind_feature(sentence)
    a = 3