import pytest
from benchmark.constraints.double_letter_constraint import DoubleLetterConstraint


@pytest.mark.parametrize('text, expected, double_letters', [
    ('Being late is never okay.', True, []),
    ('Paying your rent is not your biggest worry.', False, ['biggest', 'worry']),
    ('It\'s a big country, Tom.', True, []),
    ('That woman is creepy.', False, ['creepy']),
    ('Albert Einstein was kind of smart.', True, []),
    ('She never should have gone to that bar.', True, []),
    ('What a big house you have!', True, []),
    ('I have a lot of things to tell you.', False, ['tell']),
])
def test_double_letter_constraint(text, expected, double_letters):
    constraint = DoubleLetterConstraint()
    assert constraint.validate(text) == expected

    if not expected:
        assert len(constraint.violations) == len(double_letters)
        assert constraint.violations == double_letters
