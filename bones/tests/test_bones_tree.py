from token import DEDENT, INDENT, NAME
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


def test_flatten_tree_returns_list_of_all_tokens():
    root_node = BonesNode(None, None)
    root_tok_1 = _create_token(string='root 1')
    root_tok_2 = _create_token(string='root 2')
    root_node.tokens.append(root_tok_1)
    root_node.tokens.append(root_tok_2)

    child_1 = BonesNode(None, root_node)
    child_1_tok_1 = _create_token(string='child 1 1')
    child_1_tok_2 = _create_token(string='child 1 2')
    child_1_tok_3 = _create_token(string='child 1 3')
    child_1.tokens.append(child_1_tok_1)
    child_1.tokens.append(child_1_tok_2)
    child_1.tokens.append(child_1_tok_3)


    grand_child = BonesNode(None, parent=child_1)
    grand_child_tok_1 = _create_token(string='grand child 1')
    grand_child_tok_2 = _create_token(string='grand child 2')
    grand_child_tok_3 = _create_token(string='grand child 3')
    grand_child.tokens.append(grand_child_tok_1)
    grand_child.tokens.append(grand_child_tok_2)
    grand_child.tokens.append(grand_child_tok_3)

    child_2 = BonesNode(None, parent=root_node)
    child_2_tok_1 = _create_token(string='child 2 1')
    child_2_tok_2 = _create_token(string='child 2 2')
    child_2_tok_3 = _create_token(string='child 2 3')
    child_2_tok_4 = _create_token(string='child 2 4')
    child_2.tokens.append(child_2_tok_1)
    child_2.tokens.append(child_2_tok_2)
    child_2.tokens.append(child_2_tok_3)
    child_2.tokens.append(child_2_tok_4)

    child_1.children.append(grand_child)
    root_node.children.append(child_1)
    root_node.children.append(child_2)

    expected = [
        root_tok_1,
        root_tok_2,
        child_1_tok_1,
        child_1_tok_2,
        child_1_tok_3,
        grand_child_tok_1,
        grand_child_tok_2,
        grand_child_tok_3,
        child_2_tok_1,
        child_2_tok_2,
        child_2_tok_3,
        child_2_tok_4,
    ]

    actual = bones_tree.flatten(root_node)

    assert expected == actual


def _create_token(token_type=NAME, string=''):
    return TokenInfo(token_type, string, (0, 0), (0, 0), '')


@pytest.fixture
def dedent_token():
    return _create_token(DEDENT)


@pytest.fixture
def indent_token():
    return _create_token(INDENT)