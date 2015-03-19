from bones.block import FUNCTION, CLASS, BDD_BLOCK
from bones.token_parser import parse


def test_root_tokens_are_parsed_correctly(tokens_with_3_classes):
    module = parse(tokens_with_3_classes)

    assert 5 == len(module.children)
    assert 1 == len(module.children[1].children)
    assert 2 == len(module.children[2].children)
    assert 1 == len(module.children[4].children)

    assert FUNCTION == module.children[0].block_type
    assert CLASS == module.children[1].block_type
    assert CLASS == module.children[2].block_type
    assert FUNCTION == module.children[3].block_type
    assert CLASS == module.children[4].block_type


def test_bdd_blocks_are_parsed_correctly(tokens_with_bdd_blocks):
    bag_of_bones = parse(tokens_with_bdd_blocks)

    assert FUNCTION == bag_of_bones.children[0].block_type
    assert 3 == len(bag_of_bones.children[0].children)
    assert BDD_BLOCK == bag_of_bones.children[0].children[0].block_type
    assert BDD_BLOCK == bag_of_bones.children[0].children[1].block_type
    assert BDD_BLOCK == bag_of_bones.children[0].children[2].block_type


def test_when_nested_indents_then_blocks_are_parsed_correctly(tokens_with_nested_indents):
    bag_of_bones = parse(tokens_with_nested_indents)

    assert 3 == len(bag_of_bones.children)
    assert 1 == len(bag_of_bones.children[1].children)

    assert FUNCTION == bag_of_bones.children[0].block_type
    assert CLASS == bag_of_bones.children[1].block_type
    assert FUNCTION == bag_of_bones.children[2].block_type