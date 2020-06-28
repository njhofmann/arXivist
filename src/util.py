from typing import List


def get_formatted_user_input(msg: str = '') -> List[str]:
    """Returns a list of user entered arguments given in response to the given message
    :param msg: message to prompt to user
    :return: formatted and split arguments user gave in response
    """
    if msg:
        print(msg)
    return split_and_format_string(input('>'))


def split_and_format_string(to_format: str) -> List[str]:
    """Splits a string on any spaces in the string, removes any resulting empty strings, and returns a list of the split
    string.
    :param to_format: string to format
    :return: split string
    """
    return [char for char in to_format.split(' ') if char]


def format_str(string: str) -> str:
    for char in ' ':
        string = string.replace(char, '')
    return string


def is_list_of_n_ints(to_parse: List[str], n: int = -1) -> List[int]:
    """Returns if the given list of Strings is really a list of n integers
    :param to_parse: list of String to check
    :param n: supposed size of given list
    :return: given list of Strings as list of ints
    """
    if not to_parse:
        return []
    elif -1 < n != len(to_parse):  # -1 means variable length
        raise ValueError(f'given list {to_parse} must have only {n} entries')
    return [int(item) for item in to_parse]