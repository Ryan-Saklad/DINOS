import pytest

from benchmark.constraints.element_count_constraint import ElementCountConstraint
from utils.element_type import ElementType

# Test Cases for Words
@pytest.mark.parametrize("text, min_count, max_count, exact_count, case_sensitive, expected", [
    ("Sure, here you go!\nHello world", None, None, 2, True, True),  # 2 words, exact count, case-sensitive
    ("Sure, here you go!\nThis is a test", 3, None, None, True, True),  # 4 words, min count, case-sensitive
    ("Sure, here you go!\n", None, 5, None, True, True),  # 0 words, max count, case-sensitive
    ("Sure, here you go!\nOne two three", None, 2, None, True, False),  # 3 words, max count exceeded, case-sensitive
    ("Sure, here you go!\nThree words here", 5, None, None, True, False),  # 3 words, min count not met, case-sensitive
    ("Sure, here you go!\nThis has exactly five words", None, None, 5, True, True),  # 5 words, exact count, case-sensitive
    ("Sure, here you go!\nHello WORLD", None, None, 2, False, True),  # 2 words, exact count, case-insensitive
])
def test_element_count_words(text, min_count, max_count, exact_count, case_sensitive, expected):
    constraint = ElementCountConstraint(ElementType.WORDS, None, min_count, max_count, exact_count, case_sensitive)
    assert constraint.validate(text) == expected

# Test Cases for Characters
@pytest.mark.parametrize("text, min_count, max_count, exact_count, case_sensitive, expected", [
    ("Sure, here you go!\nHello", None, None, 5, True, True),  # 5 characters, exact count, case-sensitive
    ("Sure, here you go!\nHi", 1, None, None, True, True),  # 2 characters, min count, case-sensitive
    ("Sure, here you go!\n", None, 10, None, True, True),  # 0 characters, max count, case-sensitive
    ("Sure, here you go!\nPython", None, 5, None, True, False),  # 6 characters, max count exceeded, case-sensitive
    ("Sure, here you go!\nA", 2, None, None, True, False),  # 1 character, min count not met, case-sensitive
    ("Sure, here you go!\nHeLLo", None, None, 5, False, True),  # 5 characters, exact count, case-insensitive
])
def test_element_count_characters(text, min_count, max_count, exact_count, case_sensitive, expected):
    constraint = ElementCountConstraint(ElementType.CHARACTERS, None, min_count, max_count, exact_count, case_sensitive)
    assert constraint.validate(text) == expected

# Test Cases for Sentences
@pytest.mark.parametrize("text, min_count, max_count, exact_count, case_sensitive, expected", [
    ("Sure, here you go!\nThis is one. This is two.", None, None, 2, True, True),  # 2 sentences, exact count, case-sensitive
    ("Sure, here you go!\nOne sentence.", 1, None, None, True, True),  # 1 sentence, min count, case-sensitive
    ("Sure, here you go!\n", None, 2, None, True, True),  # 0 sentences, max count, case-sensitive
    ("Sure, here you go!\nFirst. Second. Third.", None, 2, None, True, False),  # 3 sentences, max count exceeded, case-sensitive
    ("Sure, here you go!\nThis is one. THIS IS TWO.", None, None, 2, False, True),  # 2 sentences, exact count, case-insensitive
])
def test_element_count_sentences(text, min_count, max_count, exact_count, case_sensitive, expected):
    constraint = ElementCountConstraint(ElementType.SENTENCES, None, min_count, max_count, exact_count, case_sensitive)
    assert constraint.validate(text) == expected

# Test Cases for Paragraphs
@pytest.mark.parametrize("text, min_count, max_count, exact_count, case_sensitive, expected", [
    ("Sure, here you go!\nPara 1.\n\nPara 2", None, None, 2, True, True),  # 2 paragraphs, exact count, case-sensitive
    ("Sure, here you go!\nSingle paragraph.", 1, None, None, True, True),  # 1 paragraph, min count, case-sensitive
    ("Sure, here you go!\n", None, 3, None, True, True),  # 0 paragraphs, max count, case-sensitive
    ("Sure, here you go!\nFirst para.\n\nSecond para.\n\nThird para.", None, 2, None, True, False),  # 3 paragraphs, max count exceeded, case-sensitive
    ("Sure, here you go!\nPara 1.\n\nPARA 2.", None, None, 2, False, True),  # 2 paragraphs, exact count, case-insensitive
])
def test_element_count_paragraphs(text, min_count, max_count, exact_count, case_sensitive, expected):
    constraint = ElementCountConstraint(ElementType.PARAGRAPHS, None, min_count, max_count, exact_count, case_sensitive)
    assert constraint.validate(text) == expected

# Test Cases for Specific Element Count
@pytest.mark.parametrize("text, element_type, element, min_count, max_count, exact_count, case_sensitive, expected", [
    ("Sure, here you go!\nthe quick brown fox jumps over the lazy dog", ElementType.WORDS, "the", None, None, 2, True, True),  # Test counting specific word, case-sensitive
    ("Sure, here you go!\nApple, Banana, Apple, Orange, Apple", ElementType.WORDS, "Apple", 2, None, None, True, True),  # Test minimum count of specific word, case-sensitive
    ("Sure, here you go!\nMississippi", ElementType.CHARACTERS, "s", None, 4, None, True, True),  # Test maximum count of specific character, case-sensitive
    ("Sure, here you go!\nHello, world! Hello, universe!", ElementType.WORDS, "Hello", None, 1, None, True, False),  # Test maximum count of specific word exceeded, case-sensitive
    ("Sure, here you go!\nParagraph 1.\n\nParagraph 2.\n\nParagraph 1 again.", ElementType.PARAGRAPHS, "Paragraph 1", None, None, 2, True, True),  # Test exact count of specific paragraph, case-sensitive
    ("Sure, here you go!\nSentence 1. Sentence 2. Sentence 3.", ElementType.SENTENCES, "Sentence", 3, None, None, True, True),  # Test minimum count of specific sentence, case-sensitive
    ("Sure, here you go!\nthe quick brown fox jumps over THE lazy dog", ElementType.WORDS, "the", None, None, 2, False, True),  # Test counting specific word, case-insensitive
])
def test_specific_element_count(text, element_type, element, min_count, max_count, exact_count, case_sensitive, expected):
    # Test counting specific elements in the response text against the specified constraints
    constraint = ElementCountConstraint(element_type, element, min_count, max_count, exact_count, case_sensitive)
    assert constraint.validate(text) == expected

# Test Case for Element Not Found
def test_element_not_found():
    text = "Sure, here you go!\nThe quick brown fox jumps over the lazy dog"
    element_type = ElementType.WORDS
    element = "cat"
    exact_count = 1
    case_sensitive = True
    # Test case where the specified element is not found in the response text
    constraint = ElementCountConstraint(element_type, element, exact_count=exact_count, case_sensitive=case_sensitive)
    assert constraint.validate(text) == False

# Test Case for Invalid Element Type
def test_invalid_element_type():
    # Test case where an invalid element type is provided to the ElementCountConstraint constructor
    with pytest.raises(ValueError):
        ElementCountConstraint("InvalidType", None, exact_count=1, case_sensitive=True)

# Test Case for Empty Element
def test_empty_element():
    # Test case where an empty element is provided to the ElementCountConstraint constructor
    constraint = ElementCountConstraint(ElementType.WORDS, "", exact_count=1, case_sensitive=True)
    assert constraint.validate("Sure, here you go!\nThe quick brown fox") == False

# Test Case for Element Count Exceeds Maximum
def test_element_count_exceeds_maximum():
    text = "Sure, here you go!\nApple, Banana, Apple, Orange, Apple"
    element_type = ElementType.WORDS
    element = "Apple"
    max_count = 2
    case_sensitive = True
    # Test case where the count of the specified element exceeds the maximum allowed count
    constraint = ElementCountConstraint(element_type, element, max_count=max_count, case_sensitive=case_sensitive)
    assert constraint.validate(text) == False

# Test Case for Element Count Below Minimum
def test_element_count_below_minimum():
    text = "Sure, here you go!\nMississippi"
    element_type = ElementType.CHARACTERS
    element = "s"
    min_count = 5
    case_sensitive = True
    # Test case where the count of the specified element is below the minimum required count
    constraint = ElementCountConstraint(element_type, element, min_count=min_count, case_sensitive=case_sensitive)
    assert constraint.validate(text) == False