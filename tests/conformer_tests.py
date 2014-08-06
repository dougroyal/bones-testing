import unittest
from unittest import TestCase
from io import StringIO
from token import NAME, OP, NEWLINE

from bones.conformer import suppress_mutations
from bones.tokengenerator import generate_tokens
from bones.token_parser import TokenParser
from bones.containers.bones_token import Token


class ConformerTests(TestCase):
    def test_string_funcdefs_are_pythonified(self):
        expected_0 = [
            Token((NAME,'def',(1, 0),(1, 3),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NAME,'_I_m_a_string_funcdef_Wheee_',(1, 4),(1, 34),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP,'(',(1, 34),(1, 35),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP,')',(1, 35),(1, 36),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((OP,':',(1, 36),(1, 37),'def "I\'m a string funcdef. Wheee!"():\n')),
            Token((NEWLINE,'\n',(1, 37),(1, 38),'def "I\'m a string funcdef. Wheee!"():\n')),
        ]

        expected_1 = [
            Token((NAME,'def',(4, 0),(4, 3),'def im_a_regular_function():\n')),
            Token((NAME,'im_a_regular_function',(4, 4),(4, 25),'def im_a_regular_function():\n')),
            Token((OP,'(',(4, 25),(4, 26),'def im_a_regular_function():\n')),
            Token((OP,')',(4, 26),(4, 27),'def im_a_regular_function():\n')),
            Token((OP,':',(4, 27),(4, 28),'def im_a_regular_function():\n')),
            Token((NEWLINE,'\n',(4, 28),(4, 29),'def im_a_regular_function():\n')),
        ]

        data = '''\
def "I'm a string funcdef. Wheee!"():
    pass

def im_a_regular_function():
    pass
'''
        bag_of_bones = _build_bag_of_bones(data)

        actual = suppress_mutations(bag_of_bones)

        self.assertEqual(expected_0, actual.funcdefs[0].signature)
        self.assertEqual(expected_1, actual.funcdefs[1].signature)


def _build_bag_of_bones(data):
    original_tokens = generate_tokens(StringIO(data))
    return TokenParser().parse_tokens(original_tokens)