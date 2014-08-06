import io

from bones.conformer import suppress_mutations
from bones.tokengenerator import generate_tokens
from bones.token_parser import TokenParser


def main():
    file = _tmp_get_file()

    original_tokens = generate_tokens(file)
    parsed_tokens = TokenParser().parse_tokens(original_tokens)
    pythonized_tokens = suppress_mutations(original_tokens, bag_of_bones=parsed_tokens)


def _tmp_get_file():
    data = '''\
def 'blah'():
    x=y=0

    then:
        x == y
    '''

    return io.StringIO(data)

if __name__ == '__main__':
    main()
