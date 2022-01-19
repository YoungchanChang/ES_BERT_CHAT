
def has_coda(word):
    # True : 받침이 없는 경우
    # False : 받침이 있는 경우
    return (ord(word[-1]) - 44032) % 28 == 0