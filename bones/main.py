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

    _run_bones_tests(open(file_name))


def _run_bones_tests(file):
    tokens = generate_tokens(file.readline)
    bones_tree_root = parse(tokens)

    healthy_bones = suppress_mutations(bones_tree_root)
    python_tokens = bones_tree.flatten(healthy_bones)
    module = untokenize(python_tokens)

    exec(compile(module, '', 'exec'))


def _fake_file():
    import io
    return io.StringIO('''\
def 'blah'():
    given:
        x = 'foo'

    when:
        y = 'bar'

    then:
        print('#'*80)
        print('executing from bones test: %s == %s' % (x, y))
        print("... erm, not actually checking the assertion yet, but we're getting there.")
        print('#'*80)
        x == y

test_blah()

    ''')


if __name__ == '__main__':
    _run_bones_tests(_fake_file())
