import pytest
from tokenize import TokenInfo, COMMENT
from bones.bones_tree import BonesNode
from bones.suppressors.known_mutants import BDD_BLOCK
from bones.suppressors.suppressor import suppress_mutations
from bones.tests.conftest import tokens_from_string

@pytest.fixture
def file_content():
    return \
'''
    then:
        pass
'''


def test_bdd_labels_are_removed(file_content):
    bdd_block = _generate_bdd_block_from_string(file_content)
    expected_tokens = _generate_expected_tokens_from_string(file_content)

    assert expected_tokens == suppress_mutations(bdd_block).tokens


def test_IndexError_is_not_raised_when_there_are_no_bdd_tokens():
    borked_bdd_block = _generate_bdd_block_from_string('')

    # this would raise an IndexError if a len() check isn't done.
    suppress_mutations(borked_bdd_block)

    assert 1 == 1


def _generate_bdd_block_from_string(file_as_string):
    bdd_block = BonesNode(block_type=BDD_BLOCK, parent=None)
    bdd_block.tokens = _list_of_bdd_tokens(file_as_string)
    return bdd_block

def _generate_expected_tokens_from_string(file_as_string):
    toks = _list_of_bdd_tokens(file_as_string)
    toks[0] = _make_comment_token(toks[0])
    return toks


def _list_of_bdd_tokens(file_as_string):
    #   0) the NL token (that is created by this test DLS and will not be a part of production code)
    #   1) an INDENT token (that belongs to the parent node)
    #  -2) the function's DEDENT token (that also belongs to the parent node)
    #  -1) the module's ENDMARKER token (that belongs to the root node)
    return list(tokens_from_string(file_as_string))[2:-2]


def _make_comment_token(tok):
    return TokenInfo(COMMENT, '#'+tok.string, tok.start, tok.end, tok.line)
