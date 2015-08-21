import pytest
import re
from token import NAME
from tokenize import TokenInfo
from bones.bones_tree import BonesNode
from bones.suppressors.known_mutants import FUNCTION, BDD_BLOCK
from bones.suppressors.suppressor import suppress_mutations
from bones.tests.conftest import tokens_from_string

@pytest.fixture
def file_content():
    return '''\
def "a sexy string function definition"(x, x):
'''


def test_normal_func_def_returned_as_is():
    expected_tokens = _generate_function_node_tokens_from_string('''\
def a_function(x):
''')
    func_block = _build_func_block(expected_tokens)

    returned = suppress_mutations(func_block)

    assert expected_tokens == returned.tokens


def test_sexy_func_def_returned_as_normal_python(file_content):
    given_tokens = _generate_function_node_tokens_from_string(file_content)
    func_block = _build_func_block(given_tokens)

    expected_tokens = _remove_invalid_name_characters(given_tokens)

    assert expected_tokens == suppress_mutations(func_block).tokens


def test_file_contents_with_bdd_children_is_prepended_with_the_word_test(file_content):
    given_tokens = _generate_function_node_tokens_from_string(file_content)

    func_block = _build_func_block(given_tokens)
    func_block.children.append(BonesNode(block_type=BDD_BLOCK, parent=func_block))

    expected_tokens = _prepend_function_with_test(given_tokens)

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


def _remove_invalid_name_characters(toks):
    new_func_name = toks[0].string[1:-1]
    new_func_name = re.sub(re.compile(r'[^0-9a-zA-Z_]+'), '_', new_func_name)
    toks[1] = TokenInfo(NAME, new_func_name, toks[1].start, toks[1].end, toks[1].line)
    return toks


def _prepend_function_with_test(toks):
    toks = _remove_invalid_name_characters(toks)
    toks[1] = TokenInfo(NAME, 'test_'+toks[0].string, toks[1].start, toks[1].end, toks[1].line)
    return toks
