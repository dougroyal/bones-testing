from bones.block import MODULE, CLASS, FUNCTION, BDD_BLOCK

from bones.suppressors.function import suppressor as function_suppressor

suppressors = {
    FUNCTION: function_suppressor,
}

def suppress_mutations(block):
    suppressors[block.block_type].suppress(block)
    for child in block.children:
        suppress_mutations(child)


