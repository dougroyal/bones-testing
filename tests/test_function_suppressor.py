from bones.bones_tree import BonesNode
from bones.suppressors.known_mutants import FUNCTION, BDD_BLOCK
from bones.suppressors.suppressor import suppress_mutations
from bones.utils import tokens_from_string


def test_normal_func_def_returned_as_is():
    expected_tokens = _generate_function_node_tokens_from_string('''\
def a_function(x):
''')
    func_block = _build_func_block(expected_tokens)

    returned = suppress_mutations(func_block)

    assert expected_tokens == returned.tokens


def test_sexy_func_def_returned_as_normal_python():
    given_tokens = _generate_function_node_tokens_from_string('''\
def "a sexy string function definition"(x, x):
''')
    func_block = _build_func_block(given_tokens)

    expected_tokens = _generate_function_node_tokens_from_string('''\
def a_sexy_string_function_definition(x, x):
''')

    returned = suppress_mutations(func_block)

    assert expected_tokens == returned.tokens


def test_string_functions_with_bdd_children_is_prepended_with_the_word_test():
    given_tokens = _generate_function_node_tokens_from_string('''\
def "a func with bdd children"(foo=None, bar=1):
''')
    func_block = _build_func_block(given_tokens)
    func_block.children.append(BonesNode(block_type=BDD_BLOCK, parent=func_block))

    expected_tokens = _generate_function_node_tokens_from_string('''\
def test_a_func_with_bdd_children(foo=None, bar=1):
''')

    returned = suppress_mutations(func_block)

    assert expected_tokens == returned.tokens


def _build_func_block(expected_tokens):
    func_block = BonesNode(block_type=FUNCTION, parent=None)
    func_block.tokens = expected_tokens
    return func_block


def _generate_function_node_tokens_from_string(s):
    # A function node in the bones tree will not have the
    #   - the module's final ENDMARKER token (that token belongs in the root node)
    #   - the functions DEDENT token (that also belongs to the parent node)
    # so, remove it here too.
    return list(tokens_from_string(s))[:-1]
