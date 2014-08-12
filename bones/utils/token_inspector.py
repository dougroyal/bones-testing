"""
Setup stuff to quickly look at output from tokenize module
"""

from tokenize import generate_tokens
from io import StringIO
from token import INDENT, DEDENT

data = '''\
def something():
    if x:
        pass
    whatever


'''

tokens = list(generate_tokens(StringIO(data).readline))

for t in tokens:
    if t.type == INDENT or t.type == DEDENT:
        print(t)
