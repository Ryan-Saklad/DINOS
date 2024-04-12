import pytest

from benchmark.constraints.isogram_constraint import IsogramConstraint


@pytest.mark.parametrize('text, expected, non_isograms', [
    ('She wasn\'t sure if she wanted to go or not.', True, []),
    ('They want Alaskan salmon for lunch.', False, ['Alaskan']),
    ('You guys like meat.', True, []),
    ('I\'ve been a big fan of yours for a long time.', False, ['been']),
    ('We can\’t get there on time.', False, ['there']),
    ('I want to meet his sister-in-law.', False, ['meet', 'sister-in-law']),
    ('Don\’t be silly, you\'re going to the game!', False, ['silly', 'going']),
    ('Can I open the door?', False, ['door'])
])
def test_isogram(text, expected, non_isograms):
    constraint = IsogramConstraint()
    assert constraint.validate(text) == expected

    if not expected:
        assert len(constraint.violations) == len(non_isograms)
        assert constraint.violations == non_isograms
