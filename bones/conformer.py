import re
from token import NAME

from bones.containers.bag_of_bones import BagOfBones
from bones.containers.funcdef import FuncDef


def suppress_mutations(bag_of_bones):
    new_bones = BagOfBones()

    for i, fn in enumerate(bag_of_bones.funcdefs):
        sig = _normalize_signature(fn.signature)
        norm_funcdef = FuncDef()
        norm_funcdef.signature = sig
        new_bones.funcdefs.append(norm_funcdef)

    return new_bones


def _normalize_signature(sig_toks):
    sig_toks.name_tok.type = NAME
    sig_toks.name_tok.value = _correct_func_name(sig_toks.name_tok.value)
    return sig_toks


def _correct_func_name(func_name):
    return re.sub(r'[^0-9a-zA-Z_]+','_', func_name)