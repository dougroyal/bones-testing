from tokenize import generate_tokens
from io import StringIO
import pytest


# For tree structure tests
##########################
@pytest.fixture
def tokens_with_3_classes():
    file_content = '''\
def an_outer_func():
    pass
class Foo():
    def some_func():
        pass
class Bar():
    def a_bar_func():
        pass
    def another_bar_func():
        pass
def another_outer_func():
    pass
class Baz():
    def __init__():
        pass
'''
    return generate_tokens(StringIO(file_content).readline)


@pytest.fixture
def tokens_with_bdd_blocks():
    file_content = '''\
def "a function definition with a string"():
    given:
        pass
    when:
        pass
    then:
        pass
'''
    return generate_tokens(StringIO(file_content).readline)


@pytest.fixture
def tokens_with_nested_indents():
    file_content = '''\
def an_outer_func():
    if True:
        pass
class Foo():
    def some_func():
        while False:
            pass
def another_outer_func():
    with some.context:
        pass
'''
    return generate_tokens(StringIO(file_content).readline)


# For token placement tests
###########################
@pytest.fixture
def normal_python():
    return '''\
from somewhere import rainbow
friends = ['dog']

def a_journey(friends):
    import yellow.brick

    return 'home'

destination = a_journey(friends)

'''


@pytest.fixture
def tokens_with_normal_python(normal_python):
    return generate_tokens(StringIO(normal_python).readline)


@pytest.fixture
def tokens_with_2_normal_functions():
    file_content = '''\
from newer import better
old = 'bad'

def new_test(thing):
    from special_date_module import is_new
    return is_new(thing)

class SneakyClass():
    """just making sure nothing here show up where it shouldn't"""
    pass

def old_test(thing):
    from special_date_module import is_old
    return is_old(thing)


good = new_test(thing) and not old_test(thing)
'''
    return generate_tokens(StringIO(file_content).readline)


@pytest.fixture
def tokens_with_a_normal_python_class():
    file_content = '''\
def a_func(thing):
    pass

class ImportantClass():
    """I'm parsed correctly"""

    def __init__(self):
        pass

def another_func():
    pass
'''
    return generate_tokens(StringIO(file_content).readline)
