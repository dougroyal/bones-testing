import io
from tokenize import generate_tokens

from bones.conformer import suppress_mutations
from bones.token_parser import TokenParser
from bones.containers.bones_token import Token as BonesToken


def main():
    file = _tmp_get_file()

    original_tokens = [BonesToken(t) for t in generate_tokens(file.readline)]
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
