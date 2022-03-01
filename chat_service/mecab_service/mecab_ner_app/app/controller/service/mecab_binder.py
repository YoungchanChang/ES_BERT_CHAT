from pathlib import Path

import numpy as np

from app.application.service.mecab_ner import MecabNer, MECAB_FEATURE
from app.application.service.mecab_parser import MecabParser
from app.application.service.mecab_storage import MecabStorage
from app.domain.mecab_domain import BindResult, BindToken
from domain.mecab_domain import MecabNerFeature
from domain.mecab_exception import MecabDataReaderException


class MecabCore(MecabNer):

    def parse(self, sentence: str):
        """
        문장 분해 후 값 돌려주는 기능
        - end_idx는 항상 1크다.
        :param sentence: 입력 문장
        :return: 파싱돈 결과
        """

        self.mecab_parsed_list = list(MecabParser(sentence=sentence).gen_mecab_compound_token_feature())

        mecab_cat_list = list(self.gen_infer_mecab_ner_feature())
        cat_idx_list=[]
        [cat_idx_list.extend(list(range(x.start_idx, x.end_idx, 1))) for x in mecab_cat_list]

        parse_result = []
        for idx, mecab_parse_item in enumerate(self.mecab_parsed_list):

            for mecab_item in mecab_cat_list:
                if idx+1 == mecab_item.end_idx:
                    parse_result.append((mecab_item.word,
                                         MecabNerFeature(word=mecab_item.word,
                                                    pos=mecab_item.pos,
                                                         start_idx=mecab_item.start_idx,
                                                         end_idx=mecab_item.end_idx,
                                                    category=mecab_item.category)))
                    if not self.DUPLICATE:
                        break
            if idx in cat_idx_list:
                continue

            parse_result.append((mecab_parse_item[MECAB_FEATURE].word, MecabNerFeature(word=mecab_parse_item[MECAB_FEATURE].word,
                                                                                       start_idx=mecab_parse_item[MECAB_FEATURE].mecab_token_compound_idx,
                                                                                       end_idx=mecab_parse_item[MECAB_FEATURE].mecab_token_compound_idx,
                                                                                  pos=mecab_parse_item[MECAB_FEATURE].pos)))
        return parse_result


    def ners(self, sentence: str):
        result = [x[MECAB_FEATURE] for x in self.parse(sentence=sentence) if x[MECAB_FEATURE].pos == self.NER_POS]
        return result


class MecabEntity(MecabCore):
    MIN_MEANING = 2
    NER_POS = "entity"
    DUPLICATE = False
    START_IDX = False

    def _set_mecab_path(self, ner_path: str) -> None:

        self.mecab_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "entities", "mecab_data")

        if self._clear_mecab_dir:
            self._clear_dir()

class MecabIntent(MecabCore):

    MIN_MEANING = 1
    NER_POS = "intent"
    ENTITY_POS_LIST = []
    INFER_ENTITY_POS_LIST = []
    DUPLICATE = True
    START_IDX = True

    def _set_mecab_path(self, ner_path: str) -> None:

        self.mecab_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "intents", "mecab_data")

        if self._clear_mecab_dir:
            self._clear_dir()


class MecabBinder:

    LARGE_CLASSIFIER = "_"
    LARGE_SEARCH_IDX = 0
    BIND_ENTITY_IDX = 1
    BIND_INTENT_IDX = 0
    BIND_SPLIT_IDX = 2

    def __init__(self):
        entity_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "entities", "entity_data")
        self.mecab_entity = MecabEntity(ner_path=str(entity_path), clear_mecab_dir=False)

        entity_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "intents", "intent_data")
        self.mecab_intent = MecabIntent(ner_path=str(entity_path), clear_mecab_dir=False, infer=False)

    def get_large_category(self, mc_all_ner):
        if self.LARGE_CLASSIFIER in mc_all_ner.category.large:
            e_bind_category = mc_all_ner.category.large.split(self.LARGE_CLASSIFIER)[self.LARGE_SEARCH_IDX]
        else:
            e_bind_category = mc_all_ner.category.large
        return e_bind_category

    def get_mean(self, mc_all_ner):
        return (mc_all_ner.start_idx + mc_all_ner.end_idx) / 2

    def get_bind(self, sentence: str):
        mc_it_ners = self.mecab_intent.ners(sentence)
        mc_en_ners = self.mecab_entity.ners(sentence)

        m_i_bind = []
        for m_i_ner in mc_it_ners:
            m_inf = np.inf
            m_e_tmp = None

            m_i_idx = self.get_mean(m_i_ner)            
            i_bind_category = self.get_large_category(m_i_ner)

            for m_e_ner in mc_en_ners:

                m_e_idx = self.get_mean(m_e_ner)
                e_bind_category = self.get_large_category(m_e_ner)

                if i_bind_category == e_bind_category:

                    en_in_diff = abs(m_e_idx - m_i_idx)
                    if en_in_diff < m_inf:
                        m_inf = en_in_diff
                        m_e_tmp = m_e_ner

            if m_e_tmp is not None:
                mc_it_ners.remove(m_i_ner)
                mc_en_ners.remove(m_e_tmp)
                m_i_bind.append([m_i_ner, m_e_tmp])
                
        bind_result = [(x[self.BIND_ENTITY_IDX].word, x[self.BIND_INTENT_IDX].word, x[self.BIND_ENTITY_IDX].end_idx) if x[self.BIND_ENTITY_IDX].end_idx >= x[self.BIND_INTENT_IDX].end_idx else
                  (x[self.BIND_ENTITY_IDX].word, x[self.BIND_INTENT_IDX].word, x[self.BIND_INTENT_IDX].end_idx)
                  for x in m_i_bind]
        return BindResult(bind_result=bind_result, intent_result=mc_it_ners, entity_result=mc_en_ners)


    def split_multi_en_in(self, sentence: str):


        mecab_parsed_list = list(MecabParser(sentence=sentence).gen_mecab_compound_token_feature())

        split_sentence = []
        start_idx = 0
        split_bind_result = self.get_bind(sentence).bind_result
        for result_item in split_bind_result:

            mecab_parsed_token = mecab_parsed_list[start_idx:result_item[self.BIND_SPLIT_IDX]]
            start_idx = result_item[self.BIND_SPLIT_IDX]
            restore_tokens = MecabStorage().reverse_compound_tokens(mecab_parsed_token)
            split_sentence.append(BindToken(split_sentence=" ".join(restore_tokens),
                                            entity=result_item[self.BIND_ENTITY_IDX],
                                            intent=result_item[self.BIND_INTENT_IDX]))
            print(restore_tokens)
        return split_sentence

if __name__ == "__main__":
    print(MecabBinder().split_multi_en_int("진주 아이유 좋아해 아이묭 좋아해"))
    # 1. 경로 다르게
    # 2. 옵션 다르게


    entity_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "entities", "entity_data")
    m_e = MecabEntity(ner_path=str(entity_path), clear_mecab_dir=False)

    test_sentence = "좋아 진주 아이유 듣는 것이 좋다 아이묭 좋아해"

    entity_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "intents", "intent_data")
    m_i = MecabIntent(ner_path=str(entity_path), clear_mecab_dir=False, infer=False)

    m_i_ners = m_i.ners(test_sentence)
    print(m_i_ners)

    m_e_ners = m_e.ners(test_sentence)
    print(m_e_ners)


    m_i_bind = []
    for m_i_ner in m_i_ners:
        m_inf = np.inf
        m_e_tmp = None
        m_i_idx = (m_i_ner.start_idx + m_i_ner.end_idx)/2

        if "_" in m_i_ner.category.large:
            i_bind_category = m_i_ner.category.large.split("_")[0]
        else:
            i_bind_category = m_i_ner.category.large

        for m_e_ner in m_e_ners:

            if "_" in m_e_ner.category.large:
                e_bind_category = m_e_ner.category.large.split("_")[0]
            else:
                e_bind_category = m_e_ner.category.large

            if i_bind_category == e_bind_category:
                m_e_idx = (m_e_ner.start_idx + m_e_ner.end_idx)/2

                m_e_i_diff = abs(m_e_idx - m_i_idx)
                if m_e_i_diff < m_inf:
                    m_inf = m_e_i_diff
                    m_e_tmp = m_e_ner

        if m_e_tmp is not None:
            m_i_ners.remove(m_i_ner)
            m_e_ners.remove(m_e_tmp)
            m_i_bind.append([m_i_ner, m_e_tmp])


    print(m_i_bind)
    result = [(x[self.BIND_ENTITY_IDX].word, x[self.BIND_INTENT_IDX].word, x[self.BIND_ENTITY_IDX].end_idx) if x[self.BIND_ENTITY_IDX].end_idx >= x[self.BIND_INTENT_IDX].end_idx else
              (x[self.BIND_ENTITY_IDX].word, x[self.BIND_INTENT_IDX].word, x[self.BIND_INTENT_IDX].end_idx)
              for x in m_i_bind]

    mecab_parsed_list = list(MecabParser(sentence=test_sentence).gen_mecab_compound_token_feature())
        # print(mecab_parsed_list)
        #
        # start_idx = 0
        # for result_item in result:
        #
        #     mecab_parsed_token = mecab_parsed_list[start_idx:result_item[2]]
        #     start_idx = result_item[2]
        #     # print([x[self.BIND_INTENT_IDX] for x in mecab_parsed_list])
        #     restore_tokens = MecabStorage().reverse_compound_tokens(mecab_parsed_token)
        #     print(restore_tokens)

    print(result)
    print(m_e_ners)
    print(m_i_ners)
    print("Y")