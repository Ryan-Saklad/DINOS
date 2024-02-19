import pytest

from benchmark.constraints.fibonacci_sequence_constraint import FibonacciSequenceConstraint
from utils.element_type import ElementType

# Test Cases for Words
@pytest.mark.parametrize("text,expected", [
    ("Hello world", True),  # 2 words
    ("This is a test", False),  # 4 words
    ("", False),  # 0 words
    ("One two three", True),  # 3 words
])
def test_fibonacci_words(text, expected):
    constraint = FibonacciSequenceConstraint(ElementType.WORDS)
    assert constraint.validate(text) == expected

# Test Cases for Characters
@pytest.mark.parametrize("text,expected", [
    ("Hello", True),  # 5 characters
    ("Hi", True),  # 2 characters
    ("", False),  # 0 characters
    ("Python", False),  # 6 characters
])
def test_fibonacci_characters(text, expected):
    constraint = FibonacciSequenceConstraint(ElementType.CHARACTERS)
    assert constraint.validate(text) == expected

# Test Cases for Sentences
@pytest.mark.parametrize("text,expected", [
    ("This is one. This is two.", True),  # 2 sentences
    ("One sentence.", True),  # 1 sentence
    ("", False),  # 0 sentences
    ("First. Second. Third.", True),  # 3 sentences
])
def test_fibonacci_sentences(text, expected):
    constraint = FibonacciSequenceConstraint(ElementType.SENTENCES)
    assert constraint.validate(text) == expected

# Test Cases for Paragraphs
@pytest.mark.parametrize("text,expected", [
    ("Para 1.\n\nPara 2", True),  # 2 paragraphs
    ("Single paragraph.", True),  # 1 paragraph
    ("", False),  # 0 paragraphs
    ("First para.\n\nSecond para.\n\nThird para.", True),  # 3 paragraphs
    ("P1.\n\nP2.\n\nP3.\n\nP4.\n\nP5.", True),  # 5 paragraphs
    ("One.\n\nTwo.\n\nThree.\n\nFour.", False),  # 4 paragraphs
    ("A single para.\nStill the same para.\nYes, still the same para.", True),  # 1 paragraph
])
def test_fibonacci_paragraphs(text, expected):
    constraint = FibonacciSequenceConstraint(ElementType.PARAGRAPHS)
    assert constraint.validate(text) == expected

# Test Case for Unsupported Element Type
def test_unsupported_element_type():
    with pytest.raises(ValueError):
        FibonacciSequenceConstraint("unsupported_type")

# Test for Edge Case: Multiple Spaces Between Words
def test_multiple_spaces():
    text = "Hello   world"
    constraint = FibonacciSequenceConstraint(ElementType.WORDS)
    assert constraint.validate(text) == True

# Test for Edge Case: Trailing Spaces in Sentences
def test_trailing_spaces_sentences():
    text = "This is one.  This is two. "
    constraint = FibonacciSequenceConstraint(ElementType.SENTENCES)
    assert constraint.validate(text) == True

# Test for Edge Case: Newlines in Paragraphs
def test_newlines_in_paragraphs():
    text = "\nPara 1.\n\nPara 2\n\nPara 3\n"
    constraint = FibonacciSequenceConstraint(ElementType.PARAGRAPHS)
    assert constraint.validate(text) == True

# Test for Edge Case: Non-String Input
def test_non_string_input():
    constraint = FibonacciSequenceConstraint(ElementType.WORDS)
    with pytest.raises(TypeError):
        constraint.validate(123)

# Test for Edge Case: Punctuation Without Spaces
def test_punctuation_without_spaces():
    text = "Hello,world."
    constraint = FibonacciSequenceConstraint(ElementType.WORDS)
    assert constraint.validate(text) == True  # Only 1 word because there's no space after the comma
