import re
from token import NAME, INDENT, OP, NEWLINE, STRING
from tokenize import COMMENT

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
        lvalue, rvalue = _extract_operands(then_block[line_num])
        new_line = {}
        for index, tok in enumerate(then_block[line_num]):
            new_line[index] = _dedent(indent_size, tok)
        pythonified[line_num] = new_line

    return pythonified


def _extract_operands(line):
    lvalue = []
    rvalue = []
    current_side = lvalue
    for tok in line:
        if tok.type == INDENT or tok.type == NEWLINE:
            continue
        elif tok.type == OP and tok.value == '==':
            current_side = rvalue
        else:
            current_side.append(tok)
    return lvalue, rvalue


def _build_assertEquals_tokens(line_num, indent_size, lvalue, rvalue):
    prefix = _build_assertEquals_prefix(indent_size, line_num)
    lvalue, curr_col = _build_lvalue(indent_size, line_num, lvalue)
    operator = [Token((OP, ',', (line_num, curr_col), (line_num, curr_col+1), None))]
    rvalue, curr_col = _build_rvalue(lvalue, curr_col, line_num, rvalue)
    postfix = _build_assertEquals_postfix(curr_col, line_num)

    return _add_line_str_tok_tokens(prefix, lvalue, operator, rvalue, postfix)


def _build_assertEquals_prefix(indent_size, line_num):
    return [
        Token((INDENT, ' ' * indent_size, (line_num, 0), (line_num, indent_size), None)),
        Token((NAME, 'self', (line_num, indent_size), (line_num, indent_size + 4), None)),
        Token((OP, '.', (line_num, indent_size + 4), (line_num, indent_size + 5), None)),
        Token((NAME, 'assertEqual', (line_num, indent_size + 5), (line_num, indent_size + 16), None)),
        Token((OP, '(', (line_num, indent_size + 16), (line_num, indent_size + 17), None))]


def _build_lvalue(indent_size, line_num, lvalue):
    curr_col = indent_size + len('self.assertEqual(')
    new_lvalue = []
    for tok in lvalue:
        next_col = curr_col+len(tok.value)
        new_lvalue.append(Token((tok.type, tok.value, (line_num, curr_col), (line_num, next_col), None)))
        curr_col = next_col
    return new_lvalue, curr_col

def _build_rvalue(lvalue, curr_col, line_num, rvalue):
    curr_col += len(build_line(lvalue)) - 1
    new_rvalue = []
    for tok in rvalue:
        next_col = curr_col+len(tok.value)
        new_rvalue.append(Token((tok.type, tok.value, (line_num, curr_col), (line_num, next_col), None)))
        curr_col = next_col
    return new_rvalue, curr_col

def _build_assertEquals_postfix(curr_col, line_num):
    return [
        Token((OP, ')', (line_num, curr_col), (line_num, curr_col + 1), None)),
        Token((NEWLINE, '\n', (line_num, curr_col + 1), (line_num, curr_col + 2), None))
    ]


def _add_line_str_tok_tokens(prefix, lvalue, operator, rvalue, postfix):
    line_toks = prefix + lvalue + operator + rvalue + postfix
    line_str = build_line(line_toks)
    for tok in line_toks:
        tok.line = line_str
    return line_toks


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