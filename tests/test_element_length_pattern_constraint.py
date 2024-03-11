import pytest
from benchmark.constraints.element_length_pattern_constraint import ElementLengthPatternConstraint
from utils.element_type import ElementType

# Test Case: Increasing word lengths within sentences
def test_increasing_word_lengths_within_sentences():
    text = "I am happy. This is a test. The quick brown fox jumps."
    constraint = ElementLengthPatternConstraint(ElementType.WORDS, ElementType.SENTENCES, increasing=True)
    assert constraint.validate(text) == True

# Test Case: Decreasing word lengths within sentences
def test_decreasing_word_lengths_within_sentences():
    text = "The quick brown fox jumps over the lazy dog. This is a test. I am happy."
    constraint = ElementLengthPatternConstraint(ElementType.WORDS, ElementType.SENTENCES, increasing=False)
    assert constraint.validate(text) == True

# Test Case: Increasing sentence lengths within paragraphs
def test_increasing_number_of_sentences_within_paragraphs():
    text = "I am happy. This is a test sentence. The quick brown fox jumps over the lazy dog.\n\nHello, world! This is another paragraph. And another. The quick brown fox jumps over the lazy dog, and the lazy dog sleeps."
    constraint = ElementLengthPatternConstraint(ElementType.SENTENCES, ElementType.PARAGRAPHS, increasing=True)
    assert constraint.validate(text) == True

# Test Case: Decreasing sentence lengths within paragraphs
def test_decreasing_sentence_lengths_within_paragraphs():
    text = "The quick brown fox jumps over the lazy dog, and the lazy dog sleeps. This is another paragraph. Hello, world!\n\nThe quick brown fox jumps over the lazy dog. This is a test sentence."
    constraint = ElementLengthPatternConstraint(ElementType.SENTENCES, ElementType.PARAGRAPHS, increasing=False)
    assert constraint.validate(text) == True

# Test Case: Word lengths not increasing within sentences
def test_word_lengths_not_increasing_within_sentences():
    text = "I am happy. This is a test. The fox jumps quickly."
    constraint = ElementLengthPatternConstraint(ElementType.WORDS, ElementType.SENTENCES, increasing=True)
    assert constraint.validate(text) == False

# Test Case: Word lengths not decreasing within sentences
def test_word_lengths_not_decreasing_within_sentences():
    text = "The quick brown fox. This is a test. I am very happy."
    constraint = ElementLengthPatternConstraint(ElementType.WORDS, ElementType.SENTENCES, increasing=False)
    assert constraint.validate(text) == False

# Test Case: Sentence lengths not increasing within paragraphs
def test_sentence_lengths_not_increasing_within_paragraphs():
    text = "I am happy. This is a test sentence. The quick brown fox jumps.\n\nHello, world! This is another paragraph. The quick brown fox jumps over the lazy dog, and the lazy dog sleeps soundly."
    constraint = ElementLengthPatternConstraint(ElementType.SENTENCES, ElementType.PARAGRAPHS, increasing=True)
    assert constraint.validate(text) == False

# Test Case: Sentence lengths not decreasing within paragraphs
def test_sentence_lengths_not_decreasing_within_paragraphs():
    text = "The quick brown fox jumps over the lazy dog, and the lazy dog sleeps. This is another paragraph with longer sentences. Hello, world!\n\nThe quick brown fox jumps. This is a test sentence. I am happy and excited."
    constraint = ElementLengthPatternConstraint(ElementType.SENTENCES, ElementType.PARAGRAPHS, increasing=False)
    assert constraint.validate(text) == False

# Test Case: Invalid element type
def test_invalid_element_type():
    with pytest.raises(ValueError):
        ElementLengthPatternConstraint(ElementType.CHARACTERS, ElementType.SENTENCES, increasing=True)

# Test Case: Invalid scope type
def test_invalid_scope_type():
    with pytest.raises(ValueError):
        ElementLengthPatternConstraint(ElementType.WORDS, ElementType.WORDS, increasing=True)

# Test Case: Invalid minimum length difference
def test_invalid_min_length_diff():
    with pytest.raises(ValueError):
        ElementLengthPatternConstraint(ElementType.WORDS, ElementType.SENTENCES, increasing=True, min_length_diff=0)