from token import STRING, NAME
import re
from tokenize import TokenInfo

INVALID_NAME_CHARS_PATTERN = re.compile(r'[^0-9a-zA-Z_]+')
DEF_TOKEN_POSITION = 0
FUNC_NAME_TOKEN_POSITION = 1


def is_found(block: list) -> bool:
    """
    Test the tokens to see if the function's name is a string rather than a standard python name.

    :param block: A function broken down into a list of TokenInfo
    :type block: list of TokenInfo

    :return: boolean based on whether the function uses a string as its function name
    :rtype: bool
    """
    return block.tokens[FUNC_NAME_TOKEN_POSITION].type == STRING


def suppress(block: list) -> list:
    """
    Convert the function's string name to a valid Python function name, and update all the function
    tokens so their TokenInfo properties match the new function name.

    :param block: A function broken down into a list of TokenInfo
    :type block: list of TokenInfo

    :return: A list of TokenInfo with a valid Python function name
    :rtype: list of TokenInfo
    """
    tok = block.tokens[1]
    old_func_name = tok.string
    new_func_name = _create_new_func_name(old_func_name)

    block.tokens[1] = TokenInfo(type=NAME, string=new_func_name, start=tok.start, end=tok.end, line=tok.line)

    return block


def _create_new_func_name(old_func_name: str) -> str:
    """
    :param old_func_name: The origional string based function name, which could contain any character.
    :type old_func_name: str

    :return: A name which conforms to the standard rules for python function names
    :rtype: str
    """
    new_func_name = old_func_name[1:-1]  # strip quotes from string ... this is why order of suppression is important.
    new_func_name = re.sub(INVALID_NAME_CHARS_PATTERN, '_', new_func_name)
    return new_func_name
