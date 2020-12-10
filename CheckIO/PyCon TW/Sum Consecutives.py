"""
You are given a list that contains solely integers (positive and negative). Your job is to sum only the numbers that
are identical and consecutive.
"""
import re
from itertools import groupby


def sum_consecutives(a):
    # SOLUTION ONE
    # return [sum(list(map(int, list(i[0]*(len(i[1])+1)) if i[1] else [i[0]]))) for i in re.findall(r'(.)(\1*)', ''.join(map(str, a)))]
    # SOLUTION TWO
    return [sum(list(group)) for key, group in groupby(a)]


if __name__ == '__main__':
    print("Example:")
    print(list(sum_consecutives([3, 3, 3, 4, 4, 5, 6, 6])))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert list(sum_consecutives([1, 1, 1, 1])) == [4]
    assert list(sum_consecutives([1, 1, 2, 2])) == [2, 4]
    assert list(sum_consecutives([1, 1, 2, 1])) == [2, 2, 1]
    assert list(sum_consecutives([3, 3, 3, 4, 4, 5, 6, 6])) == [9, 8, 5, 12]
    assert list(sum_consecutives([1])) == [1]
    assert list(sum_consecutives([])) == []
    print("Coding complete? Click 'Check' to earn cool rewards!")
