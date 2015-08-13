from bones.bones_tree import BonesNode
from bones.suppressors.known_mutants import BDD_BLOCK
from bones.suppressors.suppressor import suppress_mutations
from bones.utils import tokens_from_string


def test_bdd_labels_are_removed():

    bdd_block = _generate_bdd_block_from_string('''\
    then:
        pass
''')

    expected_tokens = _generate_expected_tokens_from_string('''\

        pass
''')

    assert expected_tokens == suppress_mutations(bdd_block).tokens


def test_IndexError_is_not_raised_when_there_are_no_bdd_tokens():
    borked_bdd_block = _generate_bdd_block_from_string('')

    # this would raise an IndexError if a len() check isn't done.
    suppress_mutations(borked_bdd_block)

    assert 1 == 1


def _generate_bdd_block_from_string(s):
    bdd_block = BonesNode(block_type=BDD_BLOCK, parent=None)
    bdd_block.tokens = list(tokens_from_string(s))
    # An actual bdd_block built by the parser will not have
    #   - an INDENT token (that belongs to the parent node)
    #   - the functions DEDENT token (that also belongs to the parent node)
    #   - the module's ENDMARKER token (that belongs to the root node)
    # so, remove them here too
    bdd_block.tokens = bdd_block.tokens[1:-2]

    return bdd_block

def _generate_expected_tokens_from_string(s):
    # A bdd node in the bones tree will not have the
    #   - an INDENT token (that token belongs in the parent node)
    #   - the module's final ENDMARKER token (that token belongs in the root node)
    #   - (the DEDENT won't exist in this example, because there's only one
    #      INDENT when the tokens are generated)
    # so, remove them here too.
    return list(tokens_from_string(s))[1:-1]
