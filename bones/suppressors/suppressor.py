from bones.suppressors.known_mutants import MODULE, CLASS, FUNCTION, BDD_BLOCK

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


def suppress_mutations(mutant):
    known_mutations = suppressors[mutant.block_type].known_mutations
    mutant = suppress_known_mutants(known_mutations, mutant)

    for i, child in enumerate(mutant.children):
        mutant.children[i] = suppress_mutations(child)

    return mutant


def suppress_known_mutants(known_mutations, mutant):
    found_mutations = []

    for mutation in known_mutations:
        if mutation.is_found(mutant):
            found_mutations.append(mutation)

    for mutation in found_mutations:
        mutant = mutation.suppress(mutant)

    return mutant


