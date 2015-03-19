from bones.suppressors.function import string_signature_mutation
from bones.suppressors.function import missing_test_prefix_mutation

def suppress(block):
    # order is important. if order is changed, we'll have to do smarter (more expensive) operations. See
    # note in string_signature_mutation
    known_mutations = [string_signature_mutation, missing_test_prefix_mutation]
    found_mutations = []

    for mutation in known_mutations:
        if mutation.is_found(block):
            found_mutations.append(mutation)

    for mutation in found_mutations:
        block = mutation.suppress(block)

    return block
