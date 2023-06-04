"""
    Description: Reformatting received data to some types.

    Author: Mikhail Shikalovskyi
    Version: 1.2
"""


def reformat_int(data: list) -> int | None:
    """ Function to convert executed data to int """
    if str(data) == "[]":
        return None
    else:
        return int(data[0][0])


def reformat_list(data: list) -> list:
    """ Function to convert executed data to list """
    result = []
    for i in data:
        result.append(i[0])
    return result


def reformat_list_3(data: list) -> [list, list]:
    """ Function to convert executed data to list """
    result1 = []
    result2 = []
    result3 = []
    for i in data:
        result1.append(i[0])
        result2.append(i[1])
        result3.append(i[2])
    return result1, result2, result3


def reformat_str(data: list) -> str:
    """ Function to convert executed data to str """
    result = ""
    if str(data) == "[]":
        return result
    elif data[0][0] is None:
        return "None"
    else:
        for i in data:
            result += i[0]
    return result
