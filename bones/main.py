"""
Usage:
    bones <FILE>
"""
from tokenize import generate_tokens, untokenize
import docopt
from bones.suppressors.suppressor import suppress_mutations
from bones.token_parser import parse
from bones import bones_tree


def main():
    args = docopt.docopt(__doc__)
    file_name = args['<FILE>']

    f = open(file_name)

    tokens = generate_tokens(f.readline)
    bones_tree_root = parse(tokens)

    healthy_bones = suppress_mutations(bones_tree_root)

    python_tokens = bones_tree.flatten(healthy_bones)

    executable_python = untokenize(python_tokens)
    exec(compile(executable_python, '', 'exec'))


if __name__ == '__main__':
    main()
