import pytest
from utils import custom_eval


@pytest.mark.parametrize(
        'input,expected',
        [
            ('10 + 10 - 5', 15),
            ('10 +10 -5', 15),
            ('10+10', 20),
            ('10-10', 0),
            ('10', 10),
            ('-10', -10),
            ('- 10', -10),
            ('+10', 10),
            ('+ 10', 10),
        ],
    )
def test_custom_eval(input, expected):
    assert custom_eval(input) == expected


@pytest.mark.parametrize(
        'input,expected',
        [
            ('10  10', None),
            ('10 * 10', None),
            ('10 / 10', None),
            ('-', None),
            ('+', None),
            ('10 + 10 10', None),
            ('some words', None),
            ('- -', None),
            ('--', None),
            ('--10', None),
            ('++10', None),
            ('++', None),
            ('+ +', None),
        ],
    )
def test_custom_eval_wrong_input(input, expected):
    assert custom_eval(input) is expected
