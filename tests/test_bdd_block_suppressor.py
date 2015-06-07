from bones.mutant import Mutant
from bones.suppressors.known_mutants import BDD_BLOCK
from bones.suppressors.bdd_block.suppressor import suppress
from bones.utils import tokens_from_string


def test_bdd_labels_are_removed():

    bdd_block = _generate_bdd_block_from_string('''\
    then:
        pass
''')

    expected_tokens = _generate_expected_tokens_from_string('''\

        pass
''')

    assert expected_tokens == suppress(bdd_block).tokens


def _generate_bdd_block_from_string(s):
    bdd_block = Mutant(block_type=BDD_BLOCK, parent=None)
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
