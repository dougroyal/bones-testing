from tokenize import TokenInfo

from bones.token_parser import parse


def test_module_tokens_are_put_in_root_block(tokens_with_normal_python):
    module = parse(tokens_with_normal_python)

    expected_module_tokens = [
        TokenInfo(type=1, string='from', start=(1, 0), end=(1, 4), line='from somewhere import rainbow\n'),
        TokenInfo(type=1, string='somewhere', start=(1, 5), end=(1, 14), line='from somewhere import rainbow\n'),
        TokenInfo(type=1, string='import', start=(1, 15), end=(1, 21), line='from somewhere import rainbow\n'),
        TokenInfo(type=1, string='rainbow', start=(1, 22), end=(1, 29), line='from somewhere import rainbow\n'),
        TokenInfo(type=4, string='\n', start=(1, 29), end=(1, 30), line='from somewhere import rainbow\n'),
        TokenInfo(type=1, string='friends', start=(2, 0), end=(2, 7), line="friends = ['dog']\n"),
        TokenInfo(type=52, string='=', start=(2, 8), end=(2, 9), line="friends = ['dog']\n"),
        TokenInfo(type=52, string='[', start=(2, 10), end=(2, 11), line="friends = ['dog']\n"),
        TokenInfo(type=3, string="'dog'", start=(2, 11), end=(2, 16), line="friends = ['dog']\n"),
        TokenInfo(type=52, string=']', start=(2, 16), end=(2, 17), line="friends = ['dog']\n"),
        TokenInfo(type=4, string='\n', start=(2, 17), end=(2, 18), line="friends = ['dog']\n"),
        TokenInfo(type=55, string='\n', start=(3, 0), end=(3, 1), line='\n'),
        TokenInfo(type=1, string='destination', start=(9, 0), end=(9, 11), line='destination = a_journey(friends)\n'),
        TokenInfo(type=52, string='=', start=(9, 12), end=(9, 13), line='destination = a_journey(friends)\n'),
        TokenInfo(type=1, string='a_journey', start=(9, 14), end=(9, 23), line='destination = a_journey(friends)\n'),
        TokenInfo(type=52, string='(', start=(9, 23), end=(9, 24), line='destination = a_journey(friends)\n'),
        TokenInfo(type=1, string='friends', start=(9, 24), end=(9, 31), line='destination = a_journey(friends)\n'),
        TokenInfo(type=52, string=')', start=(9, 31), end=(9, 32), line='destination = a_journey(friends)\n'),
        TokenInfo(type=4, string='\n', start=(9, 32), end=(9, 33), line='destination = a_journey(friends)\n'),
        TokenInfo(type=55, string='\n', start=(10, 0), end=(10, 1), line='\n'),
        TokenInfo(type=0, string='', start=(11, 0), end=(11, 0), line=''),
    ]

    assert module.tokens == expected_module_tokens


def test_function_tokens_are_put_in_function_blocks(tokens_with_2_normal_functions):
    module = parse(tokens_with_2_normal_functions)

    expected_function_1_tokens = [
        TokenInfo(type=1, string='def', start=(4, 0), end=(4, 3), line='def new_test(thing):\n'),
        TokenInfo(type=1, string='new_test', start=(4, 4), end=(4, 12), line='def new_test(thing):\n'),
        TokenInfo(type=52, string='(', start=(4, 12), end=(4, 13), line='def new_test(thing):\n'),
        TokenInfo(type=1, string='thing', start=(4, 13), end=(4, 18), line='def new_test(thing):\n'),
        TokenInfo(type=52, string=')', start=(4, 18), end=(4, 19), line='def new_test(thing):\n'),
        TokenInfo(type=52, string=':', start=(4, 19), end=(4, 20), line='def new_test(thing):\n'),
        TokenInfo(type=4, string='\n', start=(4, 20), end=(4, 21), line='def new_test(thing):\n'),
        TokenInfo(type=5, string='    ', start=(5, 0), end=(5, 4), line='    from special_date_module import is_new\n'),
        TokenInfo(type=1, string='from', start=(5, 4), end=(5, 8), line='    from special_date_module import is_new\n'),
        TokenInfo(type=1, string='special_date_module', start=(5, 9), end=(5, 28), line='    from special_date_module import is_new\n'),
        TokenInfo(type=1, string='import', start=(5, 29), end=(5, 35), line='    from special_date_module import is_new\n'),
        TokenInfo(type=1, string='is_new', start=(5, 36), end=(5, 42), line='    from special_date_module import is_new\n'),
        TokenInfo(type=4, string='\n', start=(5, 42), end=(5, 43), line='    from special_date_module import is_new\n'),
        TokenInfo(type=1, string='return', start=(6, 4), end=(6, 10), line='    return is_new(thing)\n'),
        TokenInfo(type=1, string='is_new', start=(6, 11), end=(6, 17), line='    return is_new(thing)\n'),
        TokenInfo(type=52, string='(', start=(6, 17), end=(6, 18), line='    return is_new(thing)\n'),
        TokenInfo(type=1, string='thing', start=(6, 18), end=(6, 23), line='    return is_new(thing)\n'),
        TokenInfo(type=52, string=')', start=(6, 23), end=(6, 24), line='    return is_new(thing)\n'),
        TokenInfo(type=4, string='\n', start=(6, 24), end=(6, 25), line='    return is_new(thing)\n'),
        TokenInfo(type=55, string='\n', start=(7, 0), end=(7, 1), line='\n'),
        TokenInfo(type=6, string='', start=(8, 0), end=(8, 0), line='class SneakyClass():\n'),
    ]

    expected_function_2_tokens = [
        TokenInfo(type=1, string='def', start=(12, 0), end=(12, 3), line='def old_test(thing):\n'),
        TokenInfo(type=1, string='old_test', start=(12, 4), end=(12, 12), line='def old_test(thing):\n'),
        TokenInfo(type=52, string='(', start=(12, 12), end=(12, 13), line='def old_test(thing):\n'),
        TokenInfo(type=1, string='thing', start=(12, 13), end=(12, 18), line='def old_test(thing):\n'),
        TokenInfo(type=52, string=')', start=(12, 18), end=(12, 19), line='def old_test(thing):\n'),
        TokenInfo(type=52, string=':', start=(12, 19), end=(12, 20), line='def old_test(thing):\n'),
        TokenInfo(type=4, string='\n', start=(12, 20), end=(12, 21), line='def old_test(thing):\n'),
        TokenInfo(type=5, string='    ', start=(13, 0), end=(13, 4), line='    from special_date_module import is_old\n'),
        TokenInfo(type=1, string='from', start=(13, 4), end=(13, 8), line='    from special_date_module import is_old\n'),
        TokenInfo(type=1, string='special_date_module', start=(13, 9), end=(13, 28), line='    from special_date_module import is_old\n'),
        TokenInfo(type=1, string='import', start=(13, 29), end=(13, 35), line='    from special_date_module import is_old\n'),
        TokenInfo(type=1, string='is_old', start=(13, 36), end=(13, 42), line='    from special_date_module import is_old\n'),
        TokenInfo(type=4, string='\n', start=(13, 42), end=(13, 43), line='    from special_date_module import is_old\n'),
        TokenInfo(type=1, string='return', start=(14, 4), end=(14, 10), line='    return is_old(thing)\n'),
        TokenInfo(type=1, string='is_old', start=(14, 11), end=(14, 17), line='    return is_old(thing)\n'),
        TokenInfo(type=52, string='(', start=(14, 17), end=(14, 18), line='    return is_old(thing)\n'),
        TokenInfo(type=1, string='thing', start=(14, 18), end=(14, 23), line='    return is_old(thing)\n'),
        TokenInfo(type=52, string=')', start=(14, 23), end=(14, 24), line='    return is_old(thing)\n'),
        TokenInfo(type=4, string='\n', start=(14, 24), end=(14, 25), line='    return is_old(thing)\n'),
        TokenInfo(type=55, string='\n', start=(15, 0), end=(15, 1), line='\n'),
        TokenInfo(type=55, string='\n', start=(16, 0), end=(16, 1), line='\n'),
        TokenInfo(type=6, string='', start=(17, 0), end=(17, 0), line='good = new_test(thing) and not old_test(thing)\n'),
    ]

    assert module.children[0].tokens == expected_function_1_tokens
    assert module.children[2].tokens == expected_function_2_tokens


def test_class_tokens_are_put_in_class_block(tokens_with_a_normal_python_class):
    module = parse(tokens_with_a_normal_python_class)

    expected_class_tokens = [
        TokenInfo(type=1, string='class', start=(4, 0), end=(4, 5), line='class ImportantClass():\n'),
        TokenInfo(type=1, string='ImportantClass', start=(4, 6), end=(4, 20), line='class ImportantClass():\n'),
        TokenInfo(type=52, string='(', start=(4, 20), end=(4, 21), line='class ImportantClass():\n'),
        TokenInfo(type=52, string=')', start=(4, 21), end=(4, 22), line='class ImportantClass():\n'),
        TokenInfo(type=52, string=':', start=(4, 22), end=(4, 23), line='class ImportantClass():\n'),
        TokenInfo(type=4, string='\n', start=(4, 23), end=(4, 24), line='class ImportantClass():\n'),
        TokenInfo(type=5, string='    ', start=(5, 0), end=(5, 4), line='    """I\'m parsed correctly"""\n'),
        TokenInfo(type=3, string='"""I\'m parsed correctly"""', start=(5, 4), end=(5, 30), line='    """I\'m parsed correctly"""\n'),
        TokenInfo(type=4, string='\n', start=(5, 30), end=(5, 31), line='    """I\'m parsed correctly"""\n'),
        TokenInfo(type=55, string='\n', start=(6, 0), end=(6, 1), line='\n'),
        TokenInfo(type=6, string='', start=(10, 0), end=(10, 0), line='def another_func():\n'),
    ]

    assert module.children[1].tokens == expected_class_tokens