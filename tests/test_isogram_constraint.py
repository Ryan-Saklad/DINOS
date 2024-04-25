import pytest

from benchmark.constraints.isogram_constraint import IsogramConstraint


@pytest.mark.parametrize('text, expected, non_isograms', [
    ('Sure, here you go!\nShe wasn\'t sure if she wanted to go or not.', True, []),
    ('Sure, here you go!\nThey want Alaskan salmon for lunch.', False, ['Alaskan']),
    ('Sure, here you go!\nYou guys like meat.', True, []),
    ('Sure, here you go!\nI\'ve been a big fan of yours for a long time.', False, ['been']),
    ('Sure, here you go!\nWe can\’t get there on time.', False, ['there']),
    ('Sure, here you go!\nI want to meet his sister-in-law.', False, ['meet', 'sister-in-law']),
    ('Sure, here you go!\nDon\’t be silly, you\'re going to the game!', False, ['silly', 'going']),
    ('Sure, here you go!\nCan I open the door?', False, ['door'])
])
def test_isogram(text, expected, non_isograms):
    constraint = IsogramConstraint()
    assert constraint.validate(text) == expected

    if not expected:
        assert len(constraint.violations) == len(non_isograms)
        assert constraint.violations == non_isograms
