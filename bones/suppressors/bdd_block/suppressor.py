from bones.suppressors.bdd_block import remove_bdd_block_labels, dedent_if_necessary


def suppress(alpha_mutant):
    known_mutations = [remove_bdd_block_labels, dedent_if_necessary]
    found_mutations = []

    for mutation in known_mutations:
        if mutation.is_found(alpha_mutant):
            found_mutations.append(mutation)

    for mutation in found_mutations:
        alpha_mutant = mutation.suppress(alpha_mutant)

    return alpha_mutant
