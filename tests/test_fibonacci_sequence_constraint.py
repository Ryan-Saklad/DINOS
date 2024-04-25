import pytest

from benchmark.constraints.fibonacci_sequence_constraint import FibonacciSequenceConstraint
from utils.element_type import ElementType

# Test Cases for Words
@pytest.mark.parametrize("text,expected", [
    ("Sure, here you go!\nHello world", True),  # 2 words
    ("Sure, here you go!\nThis is a test", False),  # 4 words
    ("Sure, here you go!\n", False),  # 0 words
    ("Sure, here you go!\nOne two three", True),  # 3 words
])
def test_fibonacci_words(text, expected):
    constraint = FibonacciSequenceConstraint(ElementType.WORDS)
    assert constraint.validate(text) == expected

# Test Cases for Characters
@pytest.mark.parametrize("text,expected", [
    ("Sure, here you go!\nHello", True),  # 5 characters
    ("Sure, here you go!\nHi", True),  # 2 characters
    ("Sure, here you go!\n", False),  # 0 characters
    ("Sure, here you go!\nPython", False),  # 6 characters
])
def test_fibonacci_characters(text, expected):
    constraint = FibonacciSequenceConstraint(ElementType.CHARACTERS)
    assert constraint.validate(text) == expected

# Test Cases for Sentences
@pytest.mark.parametrize("text,expected", [
    ("Sure, here you go!\nThis is one. This is two.", True),  # 2 sentences
    ("Sure, here you go!\nOne sentence.", True),  # 1 sentence
    ("Sure, here you go!\n", False),  # 0 sentences
    ("Sure, here you go!\nFirst. Second. Third.", True),  # 3 sentences
])
def test_fibonacci_sentences(text, expected):
    constraint = FibonacciSequenceConstraint(ElementType.SENTENCES)
    assert constraint.validate(text) == expected

# Test Cases for Paragraphs
@pytest.mark.parametrize("text,expected", [
    ("Sure, here you go!\nPara 1.\n\nPara 2", True),  # 2 paragraphs
    ("Sure, here you go!\nSingle paragraph.", True),  # 1 paragraph
    ("Sure, here you go!\n", False),  # 0 paragraphs
    ("Sure, here you go!\nFirst para.\n\nSecond para.\n\nThird para.", True),  # 3 paragraphs
    ("Sure, here you go!\nP1.\n\nP2.\n\nP3.\n\nP4.\n\nP5.", True),  # 5 paragraphs
    ("Sure, here you go!\nOne.\n\nTwo.\n\nThree.\n\nFour.", False),  # 4 paragraphs
    ("Sure, here you go!\nA single para.\nStill the same para.\nYes, still the same para.", True),  # 1 paragraph
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
    text = "Sure, here you go!\nHello   world"
    constraint = FibonacciSequenceConstraint(ElementType.WORDS)
    assert constraint.validate(text) == True

# Test for Edge Case: Trailing Spaces in Sentences
def test_trailing_spaces_sentences():
    text = "Sure, here you go!\nThis is one.  This is two. "
    constraint = FibonacciSequenceConstraint(ElementType.SENTENCES)
    assert constraint.validate(text) == True

# Test for Edge Case: Newlines in Paragraphs
def test_newlines_in_paragraphs():
    text = "Sure, here you go!\n\nPara 1.\n\nPara 2\n\nPara 3\n"
    constraint = FibonacciSequenceConstraint(ElementType.PARAGRAPHS)
    assert constraint.validate(text) == True

# Test for Edge Case: Non-String Input
def test_non_string_input():
    constraint = FibonacciSequenceConstraint(ElementType.WORDS)
    with pytest.raises(TypeError):
        constraint.validate(123)

# Test for Edge Case: Punctuation Without Spaces
def test_punctuation_without_spaces():
    text = "Sure, here you go!\nHello,world."
    constraint = FibonacciSequenceConstraint(ElementType.WORDS)
    assert constraint.validate(text) == True  # Only 1 word because there's no space after the comma
