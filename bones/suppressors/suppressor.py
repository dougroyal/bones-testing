from bones.mutant import MODULE, CLASS, FUNCTION, BDD_BLOCK

from bones.suppressors.function import suppressor as function_suppressor
from bones.suppressors.module import suppressor as module_suppressor
from bones.suppressors.bdd_block import suppressor as bdd_block_suppressor
from bones.suppressors.clazz import suppressor as class_suppressor

suppressors = {
    FUNCTION: function_suppressor,
    MODULE: module_suppressor,
    BDD_BLOCK: bdd_block_suppressor,
    CLASS: class_suppressor,
}

def suppress_mutations(alpha_mutant):
    suppressors[alpha_mutant.block_type].suppress(alpha_mutant)
    for child in alpha_mutant.children:
        suppress_mutations(child)

    return alpha_mutant


