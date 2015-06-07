from copy import copy
from pprint import pprint
from token import INDENT, NAME, OP, NEWLINE
from tokenize import TokenInfo, COMMENT, NL
import pytest
from bones.mutant import Mutant
from bones.suppressors.known_mutants import BDD_BLOCK
from bones.suppressors.bdd_block.suppressor import suppress
from bones.utils import print_tokens, tokens_from_string


def test_bdd_labels_are_removed():

    given_tokens = [
        TokenInfo(type=NAME, string='then', start=(3, 4), end=(3, 8), line='    then:\n'),
        TokenInfo(type=OP, string=':', start=(3, 8), end=(3, 9), line='    then:\n'),
        TokenInfo(type=NEWLINE, string='\n', start=(3, 9), end=(3, 10), line='    then:\n'),
        TokenInfo(type=INDENT, string='        ', start=(4, 0), end=(4, 8), line='        pass\n'),
        TokenInfo(type=NAME, string='pass', start=(4, 8), end=(4, 12), line='        pass\n'),
        TokenInfo(type=NEWLINE, string='\n', start=(4, 12), end=(4, 13), line='        pass\n'),
    ]
    bdd_block = Mutant(block_type=BDD_BLOCK, parent=None)
    bdd_block.tokens = copy(given_tokens)
    expected_tokens = [
        TokenInfo(type=INDENT, string='        ', start=(4, 0), end=(4, 8), line='        pass\n'),
        TokenInfo(type=NAME, string='pass', start=(4, 8), end=(4, 12), line='        pass\n'),
        TokenInfo(type=NEWLINE, string='\n', start=(4, 12), end=(4, 13), line='        pass\n'),
    ]

    returned = suppress(bdd_block)

    assert expected_tokens == returned.tokens


def test_bdd_labels_are_removed():

    bdd_block = _generate_bdd_block_from_string('''\
    then:
        pass
''')

    # an bdd_block built by the parser will not have
    # an INDENT token (that belongs to the parent node)
    # the functions DEDENT token
    # the module's ENDMARKER token
    # so, remove them here too
    bdd_block.tokens = bdd_block.tokens[1:-2]

    expected_tokens = list(tokens_from_string('''\

        pass
'''))

    # a bdd node in the bones tree will not have the INDENT tokent (that token belongs in the parent node)
    # and it won't have the module's final ENDMARKER token (that token belongs in the root node)
    expected_tokens = expected_tokens[1:-1]

    returned = suppress(bdd_block)

    print('\n')
    print('#'*80)
    print('EXPECTED')
    pprint(expected_tokens)
    print('='*80)
    print('ACTUAL')
    pprint(returned.tokens)
    print('#'*80)

    assert expected_tokens == returned.tokens


def _generate_bdd_block_from_string(s):
    bdd_block = Mutant(block_type=BDD_BLOCK, parent=None)
    bdd_block.tokens = list(tokens_from_string(s))
    return bdd_block


# just here to help explore the output
def _test_deleteme():
    print_tokens('''def something():
    x = 1
    then:
        pass

'''
    )
