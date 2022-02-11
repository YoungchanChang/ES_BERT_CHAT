import _mecab
from collections import namedtuple
from typing import Generator

from mecab_ner.app.domain.entity import MecabWordFeature
from mecab_ner.app.utility.custom_error import MeCabError
from mecab_ner.app.utility.string_helper import delete_pattern_from_string

STRING_NOT_FOUND = -1

Feature = namedtuple('Feature', [
    'pos',
    'semantic',
    'has_jongseong',
    'reading',
    'type',
    'start_pos',
    'end_pos',
    'expression',
])


def _create_lattice(sentence):
    lattice = _mecab.Lattice()
    lattice.add_request_type(_mecab.MECAB_ALLOCATE_SENTENCE)  # Required
    lattice.set_sentence(sentence)

    return lattice


def _get_mecab_feature(node) -> MecabWordFeature:
    # Reference:
    # - http://taku910.github.io/mecab/learn.html
    # - https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY
    # - https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/utils/dictionary/lexicon.py

    # feature = <pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
    values = node.feature.split(',')
    assert len(values) == 8

    values = [value if value != '*' else None for value in values]
    feature = dict(zip(Feature._fields, values))
    feature['has_jongseong'] = {'T': True, 'F': False}.get(feature['has_jongseong'])

    return MecabWordFeature(node.surface, **feature)


class MeCabParser:

    """ 문장을 형태소 분석하는 클래스. 형태소 분석시 형태소 분석 토큰, 스페이스 분석 토큰의 인덱스 위치도 함께 저장 """

    type_list = ["Compound", "Inflect"]

    def __init__(self, sentence: str, dicpath=''):
        argument = ''

        if dicpath != '':
            argument = '-d %s' % dicpath

        self.tagger = _mecab.Tagger(argument)
        self.sentence = sentence
        self.sentence_token = self.sentence.split()

    def _get_space_token_idx(self, mecab_word_feature: MecabWordFeature) -> int:

        """ 스페이스로 토큰 분석한 인덱스 값 반환 """

        for idx_token, sentence_token_item in enumerate(self.sentence_token):

            index_string = sentence_token_item.find(mecab_word_feature.word)
            if index_string != STRING_NOT_FOUND:

                self.sentence_token[idx_token] = delete_pattern_from_string(sentence_token_item, mecab_word_feature.word, index_string)

                return idx_token

        return False

    def gen_mecab_token_feature(self) -> Generator:

        """ 메캅으로 형태소 분석한 토큰 제너레이터로 반환 """

        lattice = _create_lattice(self.sentence)

        if not self.tagger.parse(lattice):
            raise MeCabError(self.tagger.what())

        for mecab_token_idx, mecab_token in enumerate(lattice):
            mecab_token_feature = _get_mecab_feature(mecab_token)
            mecab_token_feature.mecab_token_idx = mecab_token_idx

            space_token_idx = self._get_space_token_idx(mecab_token_feature)
            if space_token_idx is not False:
                mecab_token_feature.space_token_idx = space_token_idx
                yield mecab_token_feature

    def gen_mecab_token_type_feature(self) -> Generator:

        """ 메캅으로 형태소 분석한 토큰 제너레이터로 반환 """

        for compound_include_item in self.gen_mecab_token_feature():
            if compound_include_item.type in self.type_list:
                compound_item_list = compound_include_item.expression.split("+")
                for compound_item in compound_item_list:
                    word, pos_tag, _ = compound_item.split("/")
                    yield word, compound_include_item

            else:
                yield compound_include_item.reading, compound_include_item

