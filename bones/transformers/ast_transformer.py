from ast import NodeTransformer, FunctionDef, arguments, arg
from bones.transformers.unittest_builder import build_assertEquals

class AddSelfArgumentToTest(NodeTransformer):

    def visit_FunctionDef(self, node):
        if node.name.startswith('test_'):
            return self._build_class_funcdef(node)
        else:
            return node

    def _build_class_funcdef(self, node):
        return FunctionDef(
            name=node.name,
            args=arguments(
                args=[arg(arg='self', annotation=None)],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[]
            ),
            body=node.body,
            decorator_list=[],
            returns=None
        )


class RewriteAssertToSelfEquals(NodeTransformer):
    def visit_Assert(self, node):
        return build_assertEquals([node.test.left, node.test.comparators[0]])