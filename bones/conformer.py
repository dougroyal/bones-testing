import re
from token import NAME

from bones.containers.bag_of_bones import BagOfBones
from bones.containers.funcdef import FuncDef


def suppress_mutations(bag_of_bones):
    new_bones = BagOfBones()

    for i, orig_funcdef in enumerate(bag_of_bones.funcdefs):
        norm_funcdef = FuncDef()

        sig = _remove_heinous_characters(orig_funcdef.signature)
        sig = _prefix_test_to_tests(orig_funcdef, sig)
        norm_funcdef.signature = sig

        new_bones.funcdefs.append(norm_funcdef)

    return new_bones


def _remove_heinous_characters(sig_toks):
    sig_toks.name_tok.type = NAME
    sig_toks.name_tok.value = _correct_func_name(sig_toks.name_tok.value)
    return sig_toks


def _prefix_test_to_tests(orig_fn, new_sig):
    if len(orig_fn.bdd_blocks['then']) > 0:
        new_sig.name_tok.value = 'test_' + new_sig.name_tok.value

    return new_sig

def _correct_func_name(func_name):
    return re.sub(r'[^0-9a-zA-Z_]+','_', func_name)