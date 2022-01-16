import _mecab
from collections import namedtuple, defaultdict
import mecab

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

PosFeature = namedtuple('PosFeature', [
    'pos',
    'semantic',
    'has_jongseong',
    'reading',
    'type',
    'start_pos',
    'end_pos',
    'expression',
    'idx_original',
    'idx_pos',
])

NODE_POS = 0
NODE_EXPRESSION = 1
IDX_POS_FEATURE = 1
IDX_TOKEN = 0
STRING_NOT_FOUND = -1
pos_split = ["Compound", "Inflect"]
noun_pos_list = ["NNG", "NNP", "UNKNOWN"]

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
    assert len(values) == 8

    values = [value if value != '*' else None for value in values]
    feature = dict(zip(Feature._fields, values))
    feature['has_jongseong'] = {'T': True, 'F': False}.get(feature['has_jongseong'])

    return Feature(**feature)


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
        return reverse_sentence


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
    idx_original = None

    for parse_token_item in parse_token:
        if parse_token_item[IDX_POS_FEATURE].type is None:
            mecab_restoration.append(parse_token_item[IDX_POS_FEATURE].idx_original, parse_token_item[IDX_POS_FEATURE].reading)
            tmp_compound = None
            continue

        if tmp_compound != parse_token_item[IDX_POS_FEATURE].reading or (idx_original != parse_token_item[IDX_POS_FEATURE].idx_original):
            mecab_restoration.append(parse_token_item[IDX_POS_FEATURE].idx_original, parse_token_item[IDX_POS_FEATURE].reading)
            tmp_compound = parse_token_item[IDX_POS_FEATURE].reading
            idx_original = parse_token_item[IDX_POS_FEATURE].idx_original

    return mecab_restoration.mecab_reverse()


class MeCabValueExtractor:
    def __init__(self, dicpath=''):
        argument = ''

        if dicpath != '':
            argument = '-d %s' % dicpath

        self.tagger = _mecab.Tagger(argument)

    def parse(self, sentence):
        sentence_space_token_list = sentence.split()
        word_feature_list = list()
        lattice = _create_lattice(sentence)

        if not self.tagger.parse(lattice):
            raise MeCabError(self.tagger.what())

        for idx_node, node in enumerate(lattice):
            node_surface, node_extract_feature = node.surface, _extract_pos_expression(node)
            for idx_token, sentence_space_token_item in enumerate(sentence_space_token_list):
                if (index_string := sentence_space_token_item.find(node_surface)) != STRING_NOT_FOUND:
                    sentence_space_token_list[idx_token] = string_replacer(sentence_space_token_item, node_surface, index_string, nofail=False)
                    word_feature_list.append((node_surface,
                                             PosFeature(pos=node_extract_feature.pos, semantic=node_extract_feature.semantic,
                                                        has_jongseong=node_extract_feature.has_jongseong, reading=node_surface,
                                                        type=node_extract_feature.type, start_pos=node_extract_feature.start_pos,
                                                        end_pos=node_extract_feature.end_pos, expression=node_extract_feature.expression,
                                                        idx_original=idx_token, idx_pos=idx_node)))
                    break
        return word_feature_list

    def gen_compound_parse(self, sentence):
        compound_include_list = self.parse(sentence)
        for compound_include_item in compound_include_list:
            if compound_include_item[IDX_POS_FEATURE].type in pos_split:
                compound_item_list = compound_include_item[IDX_POS_FEATURE].expression.split("+")
                for compound_item in compound_item_list:
                    word, pos_tag, _ = compound_item.split("/")
                    yield word, compound_include_item[IDX_POS_FEATURE]

            else:
                yield compound_include_item[IDX_POS_FEATURE].reading, compound_include_item[IDX_POS_FEATURE]


    def parse_compound(self, sentence):
        compound_parse_list = [x for x in self.gen_compound_parse(sentence)]
        return compound_parse_list

if __name__ == "__main__":
    # user_sentence, parse_sentence, restore_sentence
    #
    user_sentence = "예전 거를 탈퇴를 해서 새로 가입하라는 안내까지 받았는데 예전 약국에서 사용한 공인인증서는 사실 지금 없어요. 새로 다 받아버려서요."
    mecab_value_extractor = MeCabValueExtractor()
    compound_parse_list = mecab_value_extractor.parse_compound(user_sentence)
    noun_from_compound_list = [x for x in compound_parse_list if x[IDX_POS_FEATURE].pos in noun_pos_list]
    parse_sentence = " ".join([x[IDX_TOKEN] for x in noun_from_compound_list])
    print("user sentence : " + user_sentence)
    print("parsed sentence : " + parse_sentence)
    restore_sentence = reverse_compound_parse(noun_from_compound_list)
    print("restored sentence : " + " ".join(restore_sentence))

    if user_sentence != restore_sentence:
        print(restore_sentence)


    # mecab_parsed = mecab_value_extractor.parse(user_sentence)
    # parse_sentence = " ".join([x[IDX_TOKEN] for x in mecab_parsed])
    # restore_sentence = reverse_parse(mecab_parsed)
    # print("user sentence : " + user_sentence)
    # print("parse sentence : " + parse_sentence)
    # print("restore sentence : " + restore_sentence)

