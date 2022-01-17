"""
call_center data source : https://aihub.or.kr/aidata/30716
"""
import os
import json
import csv
import re
import mecab_value_extractor as mve
USER_SENTENCE = 1
ENTITY = 2
QA_CUSTOMER = 0
QA_SERVICE = 1
FIRST_VAL = 0
BLANK_LIST = []


def get_sentence_entities():
    for (path, dir, files) in os.walk("./"):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.json':
                print("%s/%s" % (path, filename))
                with open(path + "/" + filename, 'r', encoding='cp949') as f:
                    json_data_list = json.load(f)
                    question_list = [json_data_item for json_data_item in json_data_list if json_data_item.get('QA') == "Q"]
                    question_values = [((question_item.get('고객질문(요청)').strip() or question_item.get('상담사질문(요청)').strip()), question_item.get('개체명 ')) for question_item in question_list if question_item.get('개체명 ') != '']

    return question_values


def get_sentence_entities_qa_form():
    qa_list = []
    for (path, dir, files) in os.walk("./"):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.json':
                print("%s/%s" % (path, filename))
                is_customer_turn = False
                with open(path + "/" + filename, 'r', encoding='cp949') as f:
                    json_data_list = json.load(f)
                    qa_tmp = {}
                    tmp_talk_turn = ""

                    for json_data_item in json_data_list:

                        qa_tmp['대화셋일련번호'] = json_data_item.get('대화셋일련번호')
                        if tmp_talk_turn != json_data_item.get('대화셋일련번호'):
                            tmp_talk_turn = json_data_item.get('대화셋일련번호')

                        # 고객 질문 - 상담사 답변
                        if json_data_item.get('화자') == "고객" and json_data_item.get('QA') == "Q":

                            # 고객이 2번 말하는 경우
                            if not is_customer_turn:
                                qa_tmp['고객'] = json_data_item.get('화자')
                                qa_tmp['고객발화'] = json_data_item.get('고객질문(요청)').strip() or json_data_item.get('고객답변').strip()
                                qa_tmp['고객 개체명'] = json_data_item.get('개체명 ')
                                is_customer_turn = True
                                continue

                            if is_customer_turn:
                                qa_tmp['고객'] = json_data_item.get('화자')
                                qa_tmp['고객발화'] = qa_tmp.get('고객발화') + " " + json_data_item.get('고객질문(요청)').strip() or json_data_item.get('고객답변').strip()
                                qa_tmp['고객 개체명'] = qa_tmp.get('고객 개체명') + " " + json_data_item.get('개체명 ')

                        if json_data_item.get('화자') == "상담사" and json_data_item.get('QA') == "A":
                            qa_tmp['상담사'] = json_data_item.get('화자')
                            qa_tmp['상담사발화'] = json_data_item.get('상담사질문(요청)').strip() or json_data_item.get('상담사답변').strip()
                            qa_tmp['상담사 개체명'] = json_data_item.get('개체명 ')
                            is_customer_turn = False

                            # 상담사가 질문하고 고객이 답변하는 경우 제외
                            if qa_tmp.get('고객') != None:
                                qa_list.append(qa_tmp.values())

                            qa_tmp = {}

    return qa_list


def write_csv(csv_list):
    with open('./test_file/call_center_entity.csv', 'w', encoding='utf-8-sig', newline='') as writer_csv:
        writer = csv.writer(writer_csv, delimiter=',')
        for idx, csv_item in enumerate(csv_list):
            writer.writerow([idx, *csv_item])


def read_csv():
    with open('./test_file/call_center.csv', 'r', encoding='utf-8-sig') as reader_csv:
        reader = csv.reader(reader_csv, delimiter=',')
        return list(reader)


def read_txt():
    with open("./entity_dir/call_center_entity_mecab.txt", "r", encoding='utf-8-sig') as file:
        txt_list = file.read().splitlines()
        return sorted(list(txt_list), key=len, reverse=True)


def write_txt(txt_list):
    with open("./entity_dir/call_center_entity_mecab.txt", "w", encoding='UTF8') as file:
        for txt_item in txt_list:
            data = txt_item + "\n"
            file.write(data)


def mecab_function_test():
    mecab_value_extractor = mve.MeCabValueExtractor()
    tmp_list = []

    for csv_item in read_csv():
        is_same = False

        # Do function
        compound_parse_list = mecab_value_extractor.parse_compound(csv_item[USER_SENTENCE])
        restore_list = mve.reverse_compound_parse(compound_parse_list)
        restore_sentence = " ".join(restore_list)
        if csv_item[USER_SENTENCE] != restore_sentence:
            is_same = True

        tmp_list.append([csv_item[USER_SENTENCE], restore_sentence, is_same])
    write_csv(tmp_list)


def mecab_function_diff_test():
    mecab_value_extractor = mve.MeCabValueExtractor()
    tmp_list = []

    is_same_cnt = 0
    for idx, csv_item in enumerate(read_csv()):
        is_same = False

        # Do function
        compound_parse_list = mecab_value_extractor.parse_compound(csv_item[USER_SENTENCE])
        entity_contain_list = []

        # 1. get entity from entity dictionary
        for read_item in read_txt():
            read_value, mecab_value = read_item.split(",")

            # 1-1. check if contains pattern
            if (pattern_list := mve.contain_pattern_list(mecab_value.split(), compound_parse_list)) != BLANK_LIST:

                for pattern_item in pattern_list:
                    entity_contain_list.append(read_value)

                    # 1-2. Make blank for short word. 공인인증서가 저장된 뒤에 인증서가 저장되지 않도록 하는 코드
                    for pattern_idx_item in range(pattern_item[0], pattern_item[1], 1):
                        compound_parse_list[pattern_idx_item] = "*"

        entity_contain_list.sort()

        # 2. get saved entity
        csv_entity_list = [x.strip() for x in csv_item[2].split(",")]
        csv_entity_list.sort()

        if all(elem in entity_contain_list for elem in csv_entity_list):
            print(idx, csv_item[USER_SENTENCE])
            is_same_cnt += 1
            is_same = True

        tmp_list.append([csv_item[USER_SENTENCE], csv_item[ENTITY], ", ".join(entity_contain_list), is_same])
    print(is_same_cnt, "/", len(read_csv()))
    write_csv(tmp_list)


def str_entity_mecab():
    mecab_value_extractor = mve.MeCabValueExtractor()
    txt_list = []

    for read_item in read_txt():
        txt_list.append(read_item + "," + " ".join([x[mve.IDX_TOKEN] for x in mecab_value_extractor.parse_compound(read_item)]))

    write_txt(txt_list)


if __name__ == "__main__":
    import time
    st = time.time()
    mecab_function_diff_test()
    et = time.time()
    print(et-st)

    # # 1. get entity
    # sentence_entity = get_sentence_entities()
    # write_csv(sentence_entity)
    #
    # # 2. qa_form
    # sentence_entity = get_sentence_entities_qa_form()
    # write_csv(sentence_entity)