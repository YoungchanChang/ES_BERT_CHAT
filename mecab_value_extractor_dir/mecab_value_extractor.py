import _mecab
from collections import namedtuple, defaultdict

PosFeature = namedtuple('PosFeature', [
    'pos',
    'expression',
    'reading',
    'idx_original',
    'idx_pos',
])

FEATURE_POS = 0
FEATURE_EXPRESSION = 7
IDX_POS_FEATURE = 1
IDX_COMPOUND_POS_FEATURE = 3
IDX_TOKEN = 0
IS_COMPOUND = 2


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

def reverse_compound_parse(parse_token):
    mecab_restoration = MeCabRestoration()
    tmp_compound = None
    for parse_token_item in parse_token:
        if not parse_token_item[IS_COMPOUND]:
            mecab_restoration.append(parse_token_item[IDX_COMPOUND_POS_FEATURE].idx_original, parse_token_item[IDX_TOKEN])
            tmp_compound = None
        else:
            if tmp_compound == parse_token_item[IDX_COMPOUND_POS_FEATURE].reading:
                continue
            mecab_restoration.append(parse_token_item[IDX_COMPOUND_POS_FEATURE].idx_original, parse_token_item[IDX_COMPOUND_POS_FEATURE].reading)
            tmp_compound = parse_token_item[IDX_COMPOUND_POS_FEATURE].reading



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
                    pos_feature_list.append((node_surface, PosFeature(pos=node_extract_feature[0], expression=node_extract_feature[1], reading=node_surface, idx_original=idx_token, idx_pos=idx_node)))
                    break

        return pos_feature_list


    def get_sentence_pos(self, sentence):

        compound_include_list = self.parse(sentence)
        for compound_include_item in compound_include_list:
            if "+" in compound_include_item[IDX_POS_FEATURE].expression:
                compound_item_list = compound_include_item[IDX_POS_FEATURE].expression.split("+")
                for compound_item in compound_item_list:
                    word, pos_tag, _ = compound_item.split("/")
                    yield word, pos_tag, True, compound_include_item[IDX_POS_FEATURE]

            else:
                yield compound_include_item[IDX_POS_FEATURE].reading, compound_include_item[IDX_POS_FEATURE].pos, False, compound_include_item[IDX_POS_FEATURE]


    def parse_compound(self, sentence):
        compound_parse_list = [x for x in self.get_sentence_pos(sentence)]
        return compound_parse_list


if __name__ == "__main__":
    # user_sentence, parse_sentence, restore_sentence
    user_sentence = "나는 서울대병원에 가야했었어"
    mecab_value_extractor = MeCabValueExtractor()
    compound_parse_list = mecab_value_extractor.parse_compound(user_sentence)
    parse_sentence = " ".join([x[IDX_TOKEN] for x in compound_parse_list])
    print(parse_sentence)
    restore_sentence = reverse_compound_parse(compound_parse_list)
    print(restore_sentence)


