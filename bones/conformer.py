import re
from token import NAME, INDENT, OP, STRING, NEWLINE
from tokenize import COMMENT, NL

from bones.containers.bag_of_bones import BagOfBones
from bones.containers.bones_token import Token
from bones.containers.funcdef import FuncDef
from bones.utils.builder import build_line


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
        # TODO no reason for the if block
        if orig_funcdef.then_block:
            new_lines = _transform_then_block_to_python(orig_funcdef.then_block)
            norm_funcdef.body.update(new_lines)

        new_bones.funcdefs.append(norm_funcdef)

    return new_bones


def _transform_then_block_to_python(then_block):
    pythonified = {}
    line_numbers = iter(then_block)

    # Comment out the first line, because it's the bdd keyword label token.
    # TODO do i have to do this? can I just not include it, and decrement the lines that come after it?
    first_line_num = next(line_numbers)
    first_tok = then_block[first_line_num][0]
    indent_size = first_tok.start_col
    pythonified[first_line_num] = [_mk_comment(first_tok)]

    for line_num in line_numbers:
        new_line = _prepend_assert_to_line(then_block[line_num])
        pythonified[line_num] = _correct_line_metadata(indent_size, new_line)

    return pythonified


def _prepend_assert_to_line(line):

    # Must preserve the indent on lines that start with indents.
    insert_index = 1 if line[0].type == INDENT else 0
    #
    # def foo():
    #     then:
    #         w == x # This line WILL have an INDENT token, and we must keep it.
    #         y == z # This line will NOT have an INDENT token.
    #

    if line[0].type == NL:
        # preserve linebreaks/spacing
        return line
    else:
        line.insert(insert_index, Token((NAME, 'assert ', (line[0].line_num, 0), (line[0].line_num, 0), '')))

    return line


def _correct_line_metadata(indent_size, line):
    new_line = []
    curr_col = 0 if line[0].type == INDENT else indent_size
    for tok in line:
       new_line.append(_dedent(indent_size, curr_col, tok))
       curr_col = new_line[-1].end[1]

    line_string = build_line(new_line)
    for tok in new_line:
        tok.line = line_string

    return new_line


def _add_line_str_tok_tokens(prefix, lvalue, operator, rvalue, postfix):
    line_toks = prefix + lvalue + operator + rvalue + postfix
    line_str = build_line(line_toks)
    for tok in line_toks:
        tok.line = line_str
    return line_toks


def _dedent(indent_size, curr_col, tok):
     new_value = ' '*indent_size if (tok.type == INDENT) else tok.value
     new_start_col = (tok.start[1]) if (tok.type == INDENT) else curr_col
     new_start = (tok.start[0], new_start_col)
     new_end = (tok.end[0], len(new_value)+curr_col)

     return Token((tok.type, new_value, new_start, new_end, ''))


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
