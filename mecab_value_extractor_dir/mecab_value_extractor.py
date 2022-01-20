import _mecab
from collections import namedtuple, defaultdict
from mecab_value_extractor_dir.ner_intent_dir.utility_string import string_replacer

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


def reverse_character(parse_token):
    mecab_restoration = MeCabRestoration()
    idx_pos = None
    idx_original = None

    for parse_token_item in parse_token:
        if (parse_token_item[IDX_POS_FEATURE].idx_pos != idx_pos) or (parse_token_item[IDX_POS_FEATURE].idx_original != idx_original):
            mecab_restoration.append(parse_token_item[IDX_POS_FEATURE].idx_original, parse_token_item[IDX_POS_FEATURE].reading)
            idx_pos = parse_token_item[IDX_POS_FEATURE].idx_pos
            idx_original = parse_token_item[IDX_POS_FEATURE].idx_original

    return " ".join(mecab_restoration.mecab_reverse())


def contain_pattern_list(pattern, find_tokens):
    tmp_save_list = []
    for i in range(len(find_tokens)-len(pattern)+1):
        for j in range(len(pattern)):
            if find_tokens[i+j][IDX_TOKEN] != pattern[j]:
                break
        else:
            tmp_save_list.append((i, i+len(pattern)))
    return tmp_save_list


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


    mecab_value_extractor = MeCabValueExtractor()
    user_sentence = "예전 거를 탈퇴를 해서 새로 가입하라는 안내까지 받았는데 예전 약국에서 사용한 공인인증서는 사실 지금 없어요. 새로 다 받아버려서요."
    compound_parse_list = mecab_value_extractor.parse_compound(user_sentence)

    pattern_sentence = "공인인증서"
    pattern_val = mecab_value_extractor.parse_compound(pattern_sentence)

    # check if data contains another data
    if pattern_idx := contain_pattern_list(pattern_val, compound_parse_list):
        print(pattern_idx)

    print("user sentence : " + user_sentence)
    parse_sentence = " ".join([x[IDX_TOKEN] for x in compound_parse_list])
    print("mecab parsed sentence : " + parse_sentence)
    restore_sentence = reverse_compound_parse(compound_parse_list)
    print("restored token sentence : " + " ".join(restore_sentence))

    if user_sentence != restore_sentence:
        print(restore_sentence)


    # mecab_parsed = mecab_value_extractor.parse(user_sentence)
    # parse_sentence = " ".join([x[IDX_TOKEN] for x in mecab_parsed])
    # restore_sentence = reverse_parse(mecab_parsed)
    # print("user sentence : " + user_sentence)
    # print("parse sentence : " + parse_sentence)
    # print("restore sentence : " + restore_sentence)

