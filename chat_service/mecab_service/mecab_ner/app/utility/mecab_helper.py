
MECAB_WORD_FEATURE = 0


def contain_pattern_list(pattern, find_tokens):
    if isinstance(pattern, str):
        pattern = pattern.split()

    tmp_save_list = []

    for i in range(len(find_tokens)-len(pattern)+1):
        for j in range(len(pattern)):
            if find_tokens[i+j][MECAB_WORD_FEATURE] != pattern[j]:
                break
        else:
            tmp_save_list.append((i, i+len(pattern)))

    return tmp_save_list