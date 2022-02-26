

def delete_pattern_from_string(string, pattern, index, nofail=False):
    
    """ 문자열에서 패턴을 찾아서 *로 변환해주는 기능 """
    
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(string)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return pattern + string
    if index > len(string):  # add it to the end
        return string + pattern

    len_pattern = len(pattern)
    blank_pattern = len(pattern) * "*"
    # insert the new string between "slices" of the original
    return string[:index] + blank_pattern + string[index + len_pattern:]
