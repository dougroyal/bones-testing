from tokenize import generate_tokens as generate
from bones.containers.bones_token import Token

def generate_tokens(file) -> list:
    """
    Builds a list of Token objects similar Python's tokenize module, but with
    a couple extra properties.
    :param: file: Any object which implements readline
    :return: list: A list of Token objects
    """
    tokens = []

    for t in list(generate(file.readline)):
        tokens.append(Token(t))

    return tokens


