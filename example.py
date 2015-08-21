def look_ma_i_dont_need_the_word_test_at_the_beginning_of_my_function_name():
    given:
        a=b=0

    then:
        a == b

def "i like string function names because they're easy to read and write"():
    given:
        x = 'foo'

    when:
        y = 'bar'
        print('#'*80)
        print('executing from bones test: %s == %s' % (x, y))
        print("... erm, not actually checking the assertion yet, but we're getting there.")
        print('#'*80)

    then:
        y == x

test_i_like_string_function_names_because_they_re_easy_to_read_and_write()
