from pathlib import Path

from app.application.service.mecab_ner import MecabNer, MECAB_FEATURE
from app.application.service.mecab_parser import MecabParser
from domain.mecab_domain import MecabNerFeature
from domain.mecab_exception import MecabDataReaderException


class MecabBinder(MecabNer):

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


class MecabEntity(MecabBinder):
    MIN_MEANING = 2
    NER_POS = "entity"
    DUPLICATE = False
    START_IDX = False

    def _set_mecab_path(self, ner_path: str) -> None:

        self.mecab_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "entities", "mecab_data")

        if self._clear_mecab_dir:
            self._clear_dir()

class MecabIntent(MecabBinder):
    MIN_MEANING = 2
    NER_POS = "intent"
    DUPLICATE = True
    START_IDX = True

    def _set_mecab_path(self, ner_path: str) -> None:

        self.mecab_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "intents", "mecab_data")

        if self._clear_mecab_dir:
            self._clear_dir()


if __name__ == "__main__":
    # 1. 경로 다르게
    # 2. 옵션 다르게


    entity_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "entities", "entity_data")
    m_e = MecabEntity(ner_path=str(entity_path), clear_mecab_dir=False)

    test_sentence = "진주 아이유 들을려고 아이묭 듣는 것이 좋다"

    print(m_e.parse(test_sentence))
    print(m_e.morphs(test_sentence))
    print(m_e.ners(test_sentence))

    entity_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "intents", "intent_data")
    m_n = MecabIntent(ner_path=str(entity_path), clear_mecab_dir=False, infer=False)

    test_sentence = "진주 아이유 듣는 것이 좋다 아이묭 듣는 것이 좋다"

    print(m_n.parse(test_sentence))
    print(m_n.morphs(test_sentence))
    print(m_n.ners(test_sentence))

