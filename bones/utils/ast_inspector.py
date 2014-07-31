import io
import ast
from pprint import pprint
from ast import (Module, Load, Name, Attribute, Call, Expr, Store, Assign,
                 ClassDef, alias, Import, fix_missing_locations, FunctionDef,
                arguments, arg, Str)

from bones.utils import unparser

def dump_ast(source):
    a = ast.parse(source)
    pprint(ast.dump(a))


def exec_ast(node):
    # node = Module(body=[Import(names=[alias(name='unittest', asname=None)]), ClassDef(name='AwesomeTests', bases=[Attribute(value=Name(id='unittest', ctx=Load()), attr='TestCase', ctx=Load())], keywords=[], starargs=None, kwargs=None, body=[FunctionDef(name='test_something', args=arguments(args=[arg(arg='self', annotation=None)], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=[Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Str(s='running hi')], keywords=[], starargs=None, kwargs=None)), Expr(value=Call(func=Attribute(value=Name(id='self', ctx=Load()), attr='assertEqual', ctx=Load()), args=[Str(s='hi'), Str(s='bye')], keywords=[], starargs=None, kwargs=None))], decorator_list=[], returns=None)], decorator_list=[]), Assign(targets=[Name(id='test_suite', ctx=Store())], value=Call(func=Attribute(value=Name(id='unittest', ctx=Load()), attr='TestSuite', ctx=Load()), args=[], keywords=[], starargs=None, kwargs=None)), Expr(value=Call(func=Attribute(value=Name(id='test_suite', ctx=Load()), attr='addTest', ctx=Load()), args=[Call(func=Attribute(value=Name(id='unittest', ctx=Load()), attr='makeSuite', ctx=Load()), args=[Name(id='AwesomeTests', ctx=Load())], keywords=[], starargs=None, kwargs=None)], keywords=[], starargs=None, kwargs=None)), Assign(targets=[Name(id='runner', ctx=Store())], value=Call(func=Attribute(value=Name(id='unittest', ctx=Load()), attr='TextTestRunner', ctx=Load()), args=[], keywords=[], starargs=None, kwargs=None)), Expr(value=Call(func=Attribute(value=Name(id='runner', ctx=Load()), attr='run', ctx=Load()), args=[Name(id='test_suite', ctx=Load())], keywords=[], starargs=None, kwargs=None))])
    fixed = fix_missing_locations(node)

    exec(compile(fixed, '', 'exec'))


def unparse_ast(node):
    #node = Module(body=[Import(names=[alias(name='unittest', asname=None)]), ClassDef(name='AwesomeTests', bases=[Attribute(value=Name(id='unittest', ctx=Load()), attr='TestCase', ctx=Load())], keywords=[], starargs=None, kwargs=None, body=[FunctionDef(name='test_something', args=arguments(args=[arg(arg='self', annotation=None)], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=[Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Str(s='running hi')], keywords=[], starargs=None, kwargs=None)), Expr(value=Call(func=Attribute(value=Name(id='self', ctx=Load()), attr='assertEqual', ctx=Load()), args=[Str(s='hi'), Str(s='bye')], keywords=[], starargs=None, kwargs=None))], decorator_list=[], returns=None)], decorator_list=[]), Assign(targets=[Name(id='test_suite', ctx=Store())], value=Call(func=Attribute(value=Name(id='unittest', ctx=Load()), attr='TestSuite', ctx=Load()), args=[], keywords=[], starargs=None, kwargs=None)), Expr(value=Call(func=Attribute(value=Name(id='test_suite', ctx=Load()), attr='addTest', ctx=Load()), args=[Call(func=Attribute(value=Name(id='unittest', ctx=Load()), attr='makeSuite', ctx=Load()), args=[Name(id='AwesomeTests', ctx=Load())], keywords=[], starargs=None, kwargs=None)], keywords=[], starargs=None, kwargs=None)), Assign(targets=[Name(id='runner', ctx=Store())], value=Call(func=Attribute(value=Name(id='unittest', ctx=Load()), attr='TextTestRunner', ctx=Load()), args=[], keywords=[], starargs=None, kwargs=None)), Expr(value=Call(func=Attribute(value=Name(id='runner', ctx=Load()), attr='run', ctx=Load()), args=[Name(id='test_suite', ctx=Load())], keywords=[], starargs=None, kwargs=None))])
    fixed = fix_missing_locations(node)

    buffer = io.StringIO()
    unparser.Unparser(fixed, buffer)
    generated_code = buffer.getvalue()

    print(generated_code)

if __name__ == '__main__':
    source = '''\
import unittest

class AwesomeTests(unittest.TestCase):
    def test_something(self):
        print('running hi')
        self.assertEqual('hi', 'hi')

test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(AwesomeTests))
runner=unittest.TextTestRunner()
runner.run(test_suite)
    '''

    source = '''\
def test_something(self):
    print('hi')
'''
    dump_ast(source)
    # exec_ast(ast.parse(source))
    # unparse_ast(ast.parse(source))