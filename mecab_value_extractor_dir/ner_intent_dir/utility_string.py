NO_JONGSUNG = 'ᴕ'

CHOSUNGS = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JOONGSUNGS = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNGS = [NO_JONGSUNG, 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
             'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

N_CHOSUNGS = 19
N_JOONGSUNGS = 21
N_JONGSUNGS = 28

FIRST_HANGUL = 0xAC00  # '가'
LAST_HANGUL = 0xD7A3  # '힣'


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


def to_jaso(s):
    result = []
    for c in s:
        if ord(c) < FIRST_HANGUL or ord(c) > LAST_HANGUL:  # if a character is a hangul
            result.append(c)
        else:
            code = ord(c) - FIRST_HANGUL
            jongsung_index = code % N_JONGSUNGS
            code //= N_JONGSUNGS
            joongsung_index = code % N_JOONGSUNGS
            code //= N_JOONGSUNGS
            chosung_index = code

            result.append(CHOSUNGS[chosung_index])
            result.append(JOONGSUNGS[joongsung_index])
            result.append(JONGSUNGS[jongsung_index])

    return ''.join(result)

def has_coda(word):
    # True : 받침이 없는 경우
    # False : 받침이 있는 경우
    return (ord(word[-1]) - 44032) % 28 == 0