"""
Usage:
    bones <FILE>
"""
from tokenize import generate_tokens
import docopt
from bones.suppressors.suppressor import suppress_mutations
from bones.token_parser import parse
from bones.utils import print_bones


def main():
    args = docopt.docopt(__doc__)
    file_name = args['<FILE>']

    f = open(file_name)

    tokens = generate_tokens(f.readline)
    bones_tree = parse(tokens)

    healthy_bones = suppress_mutations(bones_tree)

    print_bones(healthy_bones)


if __name__ == '__main__':
    main()
