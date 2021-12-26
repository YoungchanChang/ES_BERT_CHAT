import _mecab
from collections import namedtuple, defaultdict

PosFeature = namedtuple('PosFeature', [
    'pos',
    'expression',
    'idx_original',
    'idx_pos',
])

FEATURE_POS = 0
FEATURE_EXPRESSION = 7
IDX_POS_FEATURE = 1
IDX_TOKEN = 0


def _create_lattice(sentence):
    lattice = _mecab.Lattice()
    lattice.add_request_type(_mecab.MECAB_ALLOCATE_SENTENCE)  # Required
    lattice.set_sentence(sentence)

    return lattice


def _extract_pos_expression(node):
    # Reference:
    # - http://taku910.github.io/mecab/learn.html
    # - https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY
    # - https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/utils/dictionary/lexicon.py

    # feature = <pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
    values = node.feature.split(',')
    assert len(values) >= 8
    return values[FEATURE_POS], values[FEATURE_EXPRESSION]


class MeCabError(Exception):
    pass


class MeCabRestoration:
    def __init__(self):
        self.data = defaultdict(list)

    def append(self, index, sentence):
        self.data[index].append(sentence)

    def mecab_reverse(self):
        reverse_sentence = list()
        for key in sorted(self.data):
            reverse_sentence.append("".join(self.data[key]))
        return " ".join(reverse_sentence)


def string_replacer(original_string, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(original_string)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + original_string
    if index > len(original_string):  # add it to the end
        return original_string + newstring

    len_new_string = len(newstring)
    blank_string = len(newstring) * "*"
    # insert the new string between "slices" of the original
    return original_string[:index] + blank_string + original_string[index + len_new_string:]


def reverse_parse(parse_token):
    mecab_restoration = MeCabRestoration()
    for parse_token_item in parse_token:
        mecab_restoration.append(parse_token_item[IDX_POS_FEATURE].idx_original, parse_token_item[IDX_TOKEN])
    return mecab_restoration.mecab_reverse()


class MeCabValueExtractor:
    def __init__(self, dicpath=''):
        argument = ''

        if dicpath != '':
            argument = '-d %s' % dicpath

        self.tagger = _mecab.Tagger(argument)

    def parse(self, sentence):
        token_list = sentence.split()
        pos_feature_list = list()
        lattice = _create_lattice(sentence)

        if not self.tagger.parse(lattice):
            raise MeCabError(self.tagger.what())

        for idx_node, node in enumerate(lattice):
            node_surface, node_extract_feature = (node.surface, _extract_pos_expression(node))
            for idx_token, token_item in enumerate(token_list):
                if node_surface in token_item:
                    index_num = token_item.index(node_surface)
                    replace_item = string_replacer(token_item, node_surface, index_num, nofail=False)
                    token_list[idx_token] = replace_item
                    pos_feature_list.append((node_surface, PosFeature(pos=node_extract_feature[0], expression=node_extract_feature[1], idx_original=idx_token, idx_pos=idx_node)))
                    break

        return pos_feature_list


if __name__ == "__main__":
    # user_sentence, parse_sentence, restore_sentence
    user_sentence = "나는 서울대병원에 갈래"
    mecab_value_extractor = MeCabValueExtractor()
    mecab_parsed = mecab_value_extractor.parse("나는 서울대병원에 갈래")
    parse_sentence = " ".join([x[IDX_TOKEN] for x in mecab_parsed])
    restore_sentence = reverse_parse(mecab_parsed)
    print("user sentence : " + user_sentence)
    print("parse sentence : " + parse_sentence)
    print("restore sentence : " + restore_sentence)