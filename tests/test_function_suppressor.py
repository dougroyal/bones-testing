from copy import copy
from tokenize import TokenInfo
from bones.mutant import Mutant
from bones.suppressors.known_mutants import FUNCTION, BDD_BLOCK
from bones.suppressors.function.suppressor import suppress


def test_normal_func_def_returned_as_is():
    # given
    expected_tokens =[
        TokenInfo(type=1, string='def', start=(1, 0), end=(1, 3), line='def a_function():\n'),
        TokenInfo(type=1, string='a_function', start=(1, 4), end=(1, 14), line='def a_function():\n')
    ]
    func_block = Mutant(block_type=FUNCTION, parent=None)
    func_block.tokens = copy(expected_tokens)

    # when
    returned = suppress(func_block)

    # then
    assert expected_tokens == returned.tokens


def test_sexy_func_def_returned_as_normal_python():
    # given
    given_tokens =[
        TokenInfo(type=1, string='def', start=(1, 0), end=(1, 3), line='def "a sexy string function definition"():\n'),
        TokenInfo(type=3, string='"a sexy string function definition"', start=(1, 4), end=(1, 39), line='def "a sexy string function definition"():\n')
    ]
    func_block = Mutant(block_type=FUNCTION, parent=None)
    func_block.tokens = copy(given_tokens)
    expected_tokens = [
        TokenInfo(type=1, string='def', start=(1, 0), end=(1, 3), line='def "a sexy string function definition"():\n'),
        TokenInfo(type=1, string='a_sexy_string_function_definition', start=(1, 4), end=(1, 39), line='def "a sexy string function definition"():\n')
    ]

    # when
    returned = suppress(func_block)

    # then
    assert expected_tokens == returned.tokens


def test_string_functions_with_bdd_children_are_suppressed():
    # given
    given_tokens = [
        TokenInfo(type=1, string='def', start=(1, 0), end=(1, 3), line='def "a sexy test string function definition"():\n'),
        TokenInfo(type=3, string='"a sexy test string function definition"', start=(1, 4), end=(1, 44), line='def "a sexy test string function definition"():\n')
    ]

    func_block = Mutant(block_type=FUNCTION, parent=None)
    func_block.children.append(Mutant(block_type=BDD_BLOCK, parent=func_block))


    func_block.tokens = copy(given_tokens)
    expected_tokens = [
        TokenInfo(type=1, string='def', start=(1, 0), end=(1, 3), line='def "a sexy test string function definition"():\n'),
        TokenInfo(type=1, string='test_a_sexy_test_string_function_definition', start=(1, 4), end=(1, 44), line='def "a sexy test string function definition"():\n')
    ]

    # when
    returned = suppress(func_block)

    # then
    assert expected_tokens == returned.tokens