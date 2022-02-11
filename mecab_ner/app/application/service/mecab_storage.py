from collections import namedtuple, defaultdict


NODE_POS = 0
NODE_EXPRESSION = 1
IDX_POS_FEATURE = 1
IDX_TOKEN = 0

class MeCabStorage:

    """ 메캅 형태소 분석 결과를 원래대로 돌려주는 기능 """

    def __init__(self):
        self.data = defaultdict(list)

    def _append(self, index, sentence):

        """ 인덱스를 키값으로 추가 """

        self.data[index].append(sentence)

    def _mecab_reverse(self):
        reverse_sentence = list()
        for key in sorted(self.data):
            reverse_sentence.append("".join(self.data[key]))
        return reverse_sentence

    def get_reverse_parse(self, parse_token):
        for parse_token_item in parse_token:
            self._append(parse_token_item.space_token_idx, parse_token_item.word)
        return self._mecab_reverse()