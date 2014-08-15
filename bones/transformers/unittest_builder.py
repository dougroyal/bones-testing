from ast import (Module, Load, Name, Attribute, Call, Expr, Store, Assign, ClassDef, alias, Import, Str)


def build_unitest(nodes):
    return _wrap_body_in_unittest(nodes.body)

def build_assertEquals(args):
    return Expr(value=Call(func=Attribute(
                value=Name(id='self', ctx=Load()),
                attr='assertEqual', ctx=Load()),
                args=args,
                keywords=[],
                starargs=None,
                kwargs=None
                )
            )

def _wrap_body_in_unittest(body):
    return Module(body=[
    Import(names=[alias(name='unittest', asname=None)]),
    ClassDef(name='AwesomeTests',
             bases=[
                 Attribute(
                     value=Name(id='unittest', ctx=Load()),
                     attr='TestCase',
                     ctx=Load()
                 )
             ],
             keywords=[],
             starargs=None,
             kwargs=None,
             body=body,
             decorator_list=[]
    ),
    Assign(targets=[
        Name(
            id='test_suite',
            ctx=Store()
        )
    ],
           value=Call(
               func=Attribute(
                   value=Name(id='unittest', ctx=Load()),
                   attr='TestSuite', ctx=Load()
               ),
               args=[],
               keywords=[],
               starargs=None,
               kwargs=None
           )
    ),
    Expr(value=
         Call(func=
              Attribute(
                  value=Name(id='test_suite', ctx=Load()),
                  attr='addTest',
                  ctx=Load()
              ),
              args=[
                  Call(func=
                       Attribute(
                           value=Name(id='unittest', ctx=Load()),
                           attr='makeSuite',
                           ctx=Load()
                       ),
                       args=[Name(id='AwesomeTests', ctx=Load())],
                       keywords=[],
                       starargs=None,
                       kwargs=None
                  )
              ],
              keywords=[],
              starargs=None,
              kwargs=None
         )
    ),
    Assign(targets=[Name(id='runner', ctx=Store())],
           value=
           Call(func=
                Attribute(value=Name(id='unittest', ctx=Load()),
                          attr='TextTestRunner',
                          ctx=Load()
                ),
                args=[],
                keywords=[],
                starargs=None,
                kwargs=None)
    ),
    Expr(
        value=Call(
            func=Attribute(
                value=Name(id='runner', ctx=Load()),
                attr='run',
                ctx=Load()
            ),
            args=[Name(id='test_suite', ctx=Load())],
            keywords=[],
            starargs=None,
            kwargs=None)
    )
])

