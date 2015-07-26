from tokenize import TokenInfo, DEDENT
from tokenize import generate_tokens

from bones.token_parser import parse
from bones.utils import tokens_from_string
from bones.mutant import Mutant
from bones.suppressors.known_mutants import FUNCTION


def test_module_tokens_are_put_in_root_node():

    given = tokens_from_string('''\
from somewhere import rainbow
friends = ['dog']

def a_journey(friends):
    import yellow.brick

    return 'home'

destination = a_journey(friends)

''')

    expected_tokens = _generate_tokens_from_string('''\
from somewhere import rainbow
friends = ['dog']

## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
destination = a_journey(friends)

''')

    module = parse(given)

    assert module.tokens == expected_tokens


def test_function_tokens_are_put_in_function_blocks():
    # given
    given = tokens_from_string('''\
from newer import better
old = 'bad'

def new_test(thing):
    from special_date_module import is_new
    return is_new(thing)

class SneakyClass():
    """just making sure nothing here show up where it shouldn't"""
    pass

def old_test(thing):
    from special_date_module import is_old
    return is_old(thing)

good = new_test(thing) and not old_test(thing)
''')

    expected_function_1_tokens =  _generate_node_tokens_from_string('''\
## delete from test ##
## delete from test ##
## delete from test ##
def new_test(thing):
    from special_date_module import is_new
    return is_new(thing)

''')
    func_block_1 = _build_func_block(expected_function_1_tokens)

    expected_function_2_tokens =  _generate_node_tokens_from_string('''\
## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
## delete from test ##
def old_test(thing):
    from special_date_module import is_old
    return is_old(thing)

''')
    func_block_2 = _build_func_block(expected_function_2_tokens)

    # when
    module = parse(given)

    # then
    assert module.children[0].tokens[:-1] == func_block_1.tokens[:-1]
    # The dedent token (the last token) will look different because if way the test is generated
    assert module.children[0].tokens[-1] == TokenInfo(type=DEDENT, string='', start=(8, 0), end=(8, 0), line='class SneakyClass():\n')

    assert module.children[2].tokens[:-1] == func_block_2.tokens[:-1]
    # The dedent token (the last token) will look different because if way the test is generated
    assert module.children[2].tokens[-1] == TokenInfo(type=DEDENT, string='', start=(16, 0), end=(16, 0), line='good = new_test(thing) and not old_test(thing)\n')

def test_class_tokens_are_put_in_class_block():
    given = tokens_from_string('''\
def a_func(thing):
    pass

class ImportantClass():
    """I'm parsed correctly"""

    def __init__(self):
        pass

def another_func():
    pass
''')

    expected_tokens = _generate_node_tokens_from_string('''\
## delete from test ##
## delete from test ##
## delete from test ##
class ImportantClass():
    """I'm parsed correctly"""

## delete from test ##
## delete from test ##
''')

    module = parse(given)

    assert module.children[1].tokens[:-1] == expected_tokens[:-1]
    # The dedent token (the last token) will look different because if way the test is generated
    assert module.children[1].tokens[-1] == TokenInfo(type=DEDENT, string='', start=(10, 0), end=(10, 0), line='def another_func():\n')


def _generate_tokens_from_string(s):
    toks = list(tokens_from_string(s))
    return _remove_placeholder_tokens(toks)

def _remove_placeholder_tokens(toks):
    # In order to generate expected_tokens that will match the parser's behavior
    # some empty lines must be used to make tok.start and tok.end values the same.
    reduced_toks = []
    for tok in toks:
        if tok.line != '## delete from test ##\n':
            reduced_toks.append(tok)

    return reduced_toks

def _build_func_block(expected_tokens):
    func_block = Mutant(block_type=FUNCTION, parent=None)
    func_block.tokens = expected_tokens
    return func_block

def _generate_node_tokens_from_string(s):
    # A funcion or class node in the bones tree will not have the
    #   - the module's final ENDMARKER token (that token belongs in the root node)
    # so, remove it here too.
    return _generate_tokens_from_string(s)[:-1]

