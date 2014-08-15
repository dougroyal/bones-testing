import io
import ast
import argparse
from tokenize import generate_tokens, untokenize

from bones.conformer import suppress_mutations
from bones.token_parser import parse_tokens
from bones.containers.bones_token import Token as BonesToken

# TODO this will go away
from bones.transformers.unittest_builder import build_unitest
from bones.transformers.ast_transformer import AddSelfArgumentToTest, RewriteAssertToSelfEquals


def main():
    parser = _setup_parser()
    args = parser.parse_args()

    # ## For development only ###
    file = args.file if args.file else _tmp_get_file()
    ############################

    original_tokens = [BonesToken(t) for t in generate_tokens(file.readline)]
    bag_of_bones = parse_tokens(original_tokens)
    pythonized_bones = suppress_mutations(bag_of_bones)


    # TODO everything below this will go away, I just wanted to see it work.
    python_tokens = debone(pythonized_bones)
    executable_python = untokenize(python_tokens)

    nodes = ast.parse(executable_python)
    nodes = build_unitest(nodes)

    AddSelfArgumentToTest().visit(nodes)
    RewriteAssertToSelfEquals().visit(nodes)

    fixed = ast.fix_missing_locations(nodes)

    exec(compile(fixed, '', 'exec'))


def _setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', help='The name of a file with tests in it.', type=argparse.FileType('r'))
    return parser


# TODO this is going away
def debone(bones):
    tokens = []
    for funcdef in bones.funcdefs:
        tokens.extend(debone_line(funcdef.signature))
        keys = funcdef.body.keys()
        for key in keys:
            tokens.extend(debone_line(funcdef.body[key]))
    return tokens


# TODO this is going away
def debone_line(line):
    new_line = []
    for tok in line:
        new_line.append((tok.type, tok.value, tok.start, tok.end, tok.line))
    return new_line


# TODO this is going away
def _tmp_get_file():
    data = '''\
def 'blah'():
    x=y=0

    then:
        x == y
    '''

    return io.StringIO(data)