import pytest

from benchmark.constraints.element_count_constraint import ElementCountConstraint
from utils.element_type import ElementType

# Test Cases for Words
@pytest.mark.parametrize("text, min_count, max_count, exact_count, expected", [
    ("Hello world", None, None, 2, True),  # 2 words, exact count
    ("This is a test", 3, None, None, True),  # 4 words, min count
    ("", None, 5, None, True),  # 0 words, max count
    ("One two three", None, 2, None, False),  # 3 words, max count exceeded
    ("Three words here", 5, None, None, False),  # 3 words, min count not met
    ("This has exactly five words", None, None, 5, True),  # 5 words, exact count
])
def test_element_count_words(text, min_count, max_count, exact_count, expected):
    constraint = ElementCountConstraint(ElementType.WORDS, min_count, max_count, exact_count)
    assert constraint.validate(text) == expected

# Test Cases for Characters
@pytest.mark.parametrize("text, min_count, max_count, exact_count, expected", [
    ("Hello", None, None, 5, True),  # 5 characters, exact count
    ("Hi", 1, None, None, True),  # 2 characters, min count
    ("", None, 10, None, True),  # 0 characters, max count
    ("Python", None, 5, None, False),  # 6 characters, max count exceeded
    ("A", 2, None, None, False),  # 1 character, min count not met
])
def test_element_count_characters(text, min_count, max_count, exact_count, expected):
    constraint = ElementCountConstraint(ElementType.CHARACTERS, min_count, max_count, exact_count)
    assert constraint.validate(text) == expected

# Test Cases for Sentences
@pytest.mark.parametrize("text, min_count, max_count, exact_count, expected", [
    ("This is one. This is two.", None, None, 2, True),  # 2 sentences, exact count
    ("One sentence.", 1, None, None, True),  # 1 sentence, min count
    ("", None, 2, None, True),  # 0 sentences, max count
    ("First. Second. Third.", None, 2, None, False),  # 3 sentences, max count exceeded
])
def test_element_count_sentences(text, min_count, max_count, exact_count, expected):
    constraint = ElementCountConstraint(ElementType.SENTENCES, min_count, max_count, exact_count)
    assert constraint.validate(text) == expected

# Test Cases for Paragraphs
@pytest.mark.parametrize("text, min_count, max_count, exact_count, expected", [
    ("Para 1.\n\nPara 2", None, None, 2, True),  # 2 paragraphs, exact count
    ("Single paragraph.", 1, None, None, True),  # 1 paragraph, min count
    ("", None, 3, None, True),  # 0 paragraphs, max count
    ("First para.\n\nSecond para.\n\nThird para.", None, 2, None, False),  # 3 paragraphs, max count exceeded
])
def test_element_count_paragraphs(text, min_count, max_count, exact_count, expected):
    constraint = ElementCountConstraint(ElementType.PARAGRAPHS, min_count, max_count, exact_count)
    assert constraint.validate(text) == expected
