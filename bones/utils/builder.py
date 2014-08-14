from token import INDENT


def build_line(line):
    # the INDENT token is only present on the first line of a Block... so, if
    # we have the line with the INDENT block, there's no need for a padded indent string
    # otherwise, we need to build the padded string based off the start_col of the first token
    indent_string = '' if line[0].type == INDENT else ' '*line[0].start_col
    return indent_string + ''.join([tok.value for tok in line])