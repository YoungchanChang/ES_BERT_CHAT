
def has_coda(word):
    # True : 받침이 없는 경우
    # False : 받침이 있는 경우
    return (ord(word[-1]) - 44032) % 28 == 0


def get_marker(word, marker):
    josa_sbj = "이"
    if marker == "josa_sbj":
        if has_coda(word):
            josa_sbj = "가"
            return josa_sbj
        return josa_sbj

    josa_obj = "을"
    if marker == "josa_obj":
        if has_coda(word):
            josa_obj = "를"
            return josa_obj
        return josa_obj
    return False