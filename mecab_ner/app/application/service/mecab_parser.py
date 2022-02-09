import _mecab
from collections import namedtuple

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

    def __init__(self, sentence: str, dicpath=''):
        argument = ''

        if dicpath != '':
            argument = '-d %s' % dicpath

        self.tagger = _mecab.Tagger(argument)
        self.sentence = sentence
        self.sentence_token = self.sentence.split()

    def _get_idx_token(self, mecab_word_feature: MecabWordFeature) -> int:

        for idx_token, sentence_token_item in enumerate(self.sentence_token):

            index_string = sentence_token_item.find(mecab_word_feature.word)
            if index_string != STRING_NOT_FOUND:

                self.sentence_token[idx_token] = delete_pattern_from_string(sentence_token_item, mecab_word_feature.word, index_string)

                return idx_token

        return False

    def get_parse_results(self):
        mecab_parse_results = []

        lattice = _create_lattice(self.sentence)

        if not self.tagger.parse(lattice):
            raise MeCabError(self.tagger.what())

        for idx_node, node in enumerate(lattice):
            mecab_word_feature = _get_mecab_feature(node)
            mecab_word_feature.idx_pos = idx_node

            idx_token = self._get_idx_token(mecab_word_feature)
            if idx_token:
                mecab_word_feature.idx_token = idx_token
                mecab_parse_results.append(mecab_word_feature)

        return mecab_parse_results
