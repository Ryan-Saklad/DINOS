import pytest
from benchmark.constraints.double_letter_constraint import DoubleLetterConstraint


@pytest.mark.parametrize('text, expected, double_letters', [
    ('Sure, here you go!\nBeing late is never okay.', True, []),
    ('Sure, here you go!\nPaying your rent is not your biggest worry.', False, ['biggest', 'worry']),
    ('Sure, here you go!\nIt\'s a big country, Tom.', True, []),
    ('Sure, here you go!\nThat woman is creepy.', False, ['creepy']),
    ('Sure, here you go!\nAlbert Einstein was kind of smart.', True, []),
    ('Sure, here you go!\nShe never should have gone to that bar.', True, []),
    ('Sure, here you go!\nWhat a big house you have!', True, []),
    ('Sure, here you go!\nI have a lot of things to tell you.', False, ['tell']),
])
def test_double_letter_constraint(text, expected, double_letters):
    constraint = DoubleLetterConstraint()
    assert constraint.validate(text) == expected

    if not expected:
        assert len(constraint.violations) == len(double_letters)
        assert constraint.violations == double_letters
