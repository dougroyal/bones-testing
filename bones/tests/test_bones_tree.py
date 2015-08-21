from token import DEDENT, INDENT, NAME, ENDMARKER
from tokenize import TokenInfo
import pytest

from bones.bones_tree import BonesNode
from bones import bones_tree


def test_node_correctly_identifies_its_dedent_token(dedent_token, indent_token):
    node = BonesNode(None, None)

    assert False == node.is_my_dedent(dedent_token)

    node.is_my_dedent(indent_token)
    assert True == node.is_my_dedent(dedent_token)

    node.is_my_dedent(indent_token)
    node.is_my_dedent(indent_token)
    node.is_my_dedent(indent_token)
    assert False == node.is_my_dedent(dedent_token)
    assert False == node.is_my_dedent(dedent_token)
    assert True == node.is_my_dedent(dedent_token)

    assert False == node.is_my_dedent(dedent_token)


def test_flatten_tree_preserves_original_token_location():

    root_node = BonesNode(None, None)
    root_tok_1 = _create_token(string='root 1', start=(1,0))
    root_tok_2 = _create_token(string='root 2', start=(6, 0))
    endmarker = _create_token(ENDMARKER, start=(7, 0))
    root_node.tokens.append(root_tok_1)
    root_node.tokens.append(root_tok_2)
    root_node.tokens.append(endmarker)

    child = BonesNode(None, parent=root_node)
    child_tok_1 = _create_token(string='child 1', start=(2, 0))
    child_tok_2 = _create_token(string='child 2', start=(3, 0), end=(3,3))
    child_tok_3 = _create_token(string='child 3', start=(3, 3), end=(3,6))
    child_tok_4 = _create_token(string='child 4', start=(5, 0))
    child.tokens.append(child_tok_1)
    child.tokens.append(child_tok_3) # tokens on the same line should
    child.tokens.append(child_tok_2) # be sorted base on their start column
    child.tokens.append(child_tok_4)

    grand_child = BonesNode(None, parent=child)
    grand_child_tok = _create_token(string='grand child', start=(4, 0))
    grand_child.tokens.append(grand_child_tok)

    child.children.append(grand_child)
    root_node.children.append(child)

    expected = [
        root_tok_1,
        child_tok_1,
        child_tok_2,
        child_tok_3,
        grand_child_tok,
        child_tok_4,
        root_tok_2,
        endmarker
    ]

    actual = bones_tree.flatten(root_node)

    assert expected == actual


def _create_token(token_type=NAME, string='', start=(0,0), end=(0,0), line=''):
    return TokenInfo(token_type, string, start, end, line)


@pytest.fixture
def dedent_token():
    return _create_token(DEDENT)


@pytest.fixture
def indent_token():
    return _create_token(INDENT)