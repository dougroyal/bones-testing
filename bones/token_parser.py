from token import NAME
from bones.block import Block, MODULE, CLASS, FUNCTION, BDD_BLOCK, BDD_BLOCK_TYPES


def parse(tokens):
    module = Block(block_type=MODULE, parent=None)
    curr_container = module

    for index, tok in enumerate(tokens):

        if curr_container.is_my_dedent(tok):
            curr_container.tokens.append(tok)
            curr_container = curr_container.parent

        elif _is_start_of_class_block(tok):
            curr_container = Block(block_type=CLASS, parent=module)
            curr_container.tokens.append(tok)
            module.children.append(curr_container)

        elif _is_start_of_function_block(tok):
            func_block = Block(block_type=FUNCTION, parent=curr_container)
            curr_container.children.append(func_block)
            curr_container = func_block
            curr_container.tokens.append(tok)

        elif _is_start_of_bdd_block(tok):
            bdd_block = Block(block_type=BDD_BLOCK, parent=curr_container)
            curr_container.children.append(bdd_block)
            curr_container = bdd_block
            curr_container.tokens.append(tok)

        else:
            curr_container.tokens.append(tok)


    return module


def _is_start_of_class_block(tok):
    return tok.type == NAME and tok.string == 'class'


def _is_start_of_function_block(tok):
    return tok.type == NAME and tok.string == 'def'


def _is_start_of_bdd_block(tok):
    return tok.type == NAME and tok.string in BDD_BLOCK_TYPES