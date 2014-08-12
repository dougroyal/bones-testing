import re
from token import NAME, INDENT
from tokenize import COMMENT

from bones.containers.bag_of_bones import BagOfBones
from bones.containers.bones_token import Token
from bones.containers.funcdef import FuncDef


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
        if orig_funcdef.then_block:
            new_lines = _transform_then_block_to_python(orig_funcdef.then_block)
            norm_funcdef.body.update(new_lines)

        new_bones.funcdefs.append(norm_funcdef)

    return new_bones

def _transform_then_block_to_python(then_block):
    pythonified = {}
    line_numbers = iter(then_block)

    # Comment out the first line, because it's the bdd keyword label token.
    first_line_num = next(line_numbers)
    first_tok = then_block[first_line_num][0]
    indent_size = first_tok.start_col
    pythonified[first_line_num] = _mk_comment(first_tok)

    # Dedent the rest of the line tokens
    for line_num in line_numbers:
        new_line = {}
        for index, tok in enumerate(then_block[line_num]):
            new_line[index] = _dedent(indent_size, tok)
        pythonified[line_num] = new_line

    return pythonified

def _dedent(indent_size, tok):
    new_value = tok.value[:indent_size] if (tok.type == INDENT) else tok.value
    new_start_col = tok.start[1] if (tok.type == INDENT) else tok.start[1] - indent_size
    new_start = (tok.start[0], new_start_col)
    new_end = (tok.end[0], tok.end[1] - indent_size)
    new_line = tok.line[indent_size:]

    return Token((tok.type, new_value, new_start, new_end, new_line))

def _mk_comment(tok):
    return Token((COMMENT, '#'+tok.value, tok.start, tok.end, tok.line))


def _remove_heinous_characters(sig_toks):
    sig_toks.name_tok.type = NAME
    sig_toks.name_tok.value = _correct_func_name(sig_toks.name_tok.value)
    return sig_toks


def _prefix_test_to_tests(orig_fn, new_sig):
    if len(orig_fn.then_block) > 0:
        new_sig.name_tok.value = 'test_' + new_sig.name_tok.value

    return new_sig


def _correct_func_name(func_name):
    return re.sub(r'[^0-9a-zA-Z_]+','_', func_name)