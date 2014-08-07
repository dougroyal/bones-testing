import re
from token import NAME
from tokenize import COMMENT

from bones.containers.bag_of_bones import BagOfBones
from bones.containers.bones_token import Token
from bones.containers.funcdef import FuncDef


from pprint import pprint

def suppress_mutations(bag_of_bones):
    new_bones = BagOfBones()

    for i, orig_funcdef in enumerate(bag_of_bones.funcdefs):
        norm_funcdef = FuncDef()
        norm_funcdef.body = orig_funcdef.body

        # Fix funcdef signature
        sig = _remove_heinous_characters(orig_funcdef.signature)
        sig = _prefix_test_to_tests(orig_funcdef, sig)
        norm_funcdef.signature = sig

        # Fix funcdef bdd keywords
        if len(orig_funcdef.bdd_blocks['then']):
            then_kw_line_num = list(orig_funcdef.bdd_blocks['then'].keys())[0]
            then_kw_tok = orig_funcdef.bdd_blocks['then'][then_kw_line_num][0]
            norm_funcdef.body[then_kw_tok.line_num] = _mk_comment(then_kw_tok)

        # for line_num in orig_funcdef.bdd_blocks['then']:
        #     norm_funcdef.body[line_num] = _mk_comment(orig_funcdef.bdd_blocks['then'][line_num])

        new_bones.funcdefs.append(norm_funcdef)

    return new_bones

def _mk_comment(tok):
    return Token((COMMENT, '#'+tok.value, tok.start, tok.end, tok.line))

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