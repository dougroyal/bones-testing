from bones.block import MODULE, CLASS, FUNCTION, BDD_BLOCK

from bones.suppressors import module_suppressor
from bones.suppressors import class_suppressor
from bones.suppressors import function_suppressor
from bones.suppressors import bdd_suppressor

suppressors = {
    MODULE: module_suppressor,
    CLASS: class_suppressor,
    FUNCTION: function_suppressor,
    BDD_BLOCK: bdd_suppressor
}

def suppress_mutations(block):
    suppressors[block.block_type].suppress(block)
    for child in block.children:
        suppress_mutations(child)


