import pytest
from benchmark.constraints.element_repetition_constraint import ElementRepetitionConstraint
from utils.element_type import ElementType

# Test Case: Character repetition within words, case-sensitive
def test_character_repetition_within_words_case_sensitive():
    constraint = ElementRepetitionConstraint(ElementType.CHARACTERS, "a", max_repetitions=1, scope_type=ElementType.WORDS, case_sensitive=True)
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lazy dog") == True
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lAazy dog") == True
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the laazy dog") == False

# Test Case: Character repetition within words, case-insensitive
def test_character_repetition_within_words_case_insensitive():
    constraint = ElementRepetitionConstraint(ElementType.CHARACTERS, "a", max_repetitions=1, scope_type=ElementType.WORDS, case_sensitive=False)
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lazy dog") == True
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lAazy dog") == False

# Test Case: Word repetition within sentences, case-sensitive
def test_word_repetition_within_sentences_case_sensitive():
    constraint = ElementRepetitionConstraint(ElementType.WORDS, "the", min_repetitions=1, max_repetitions=2, scope_type=ElementType.SENTENCES, case_sensitive=True)
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lazy dog. The fox is quick and the dog is lazy.") == True
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lazy dog. the fox is quick and the dog is lazy and the snake exists. The fox and the dog are friends.") == False

# Test Case: Word repetition within sentences, case-insensitive
def test_word_repetition_within_sentences_case_insensitive():
    constraint = ElementRepetitionConstraint(ElementType.WORDS, "the", min_repetitions=1, max_repetitions=2, scope_type=ElementType.SENTENCES, case_sensitive=False)
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lazy dog. THE fox is quick and the dog is lazy.") == True
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lazy dog. THE fox is quick and THE dog is lazy and THE snake exists. The fox and THE dog are friends.") == False

# Test Case: Word repetition within paragraphs, case-sensitive
def test_word_repetition_within_paragraphs_case_sensitive():
    constraint = ElementRepetitionConstraint(ElementType.WORDS, "fox", min_repetitions=1, max_repetitions=3, scope_type=ElementType.PARAGRAPHS, case_sensitive=True)
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lazy dog. The fox is quick and the dog is lazy.\n\nThe fox and the dog are friends. The fox likes to play with the dog.") == True
    assert constraint.validate("Sure, here you go!\nThe quick brown fox jumps over the lazy dog. The fox is quick and the dog is lazy.\n\nThe fox and the dog are friends. The fox likes to play with the dog. The fox, the dog, and the fox are best buddies.") == False

# Test Case: Invalid element type
def test_invalid_element_type():
    with pytest.raises(ValueError):
        ElementRepetitionConstraint(ElementType.SENTENCES, "hello", max_repetitions=1)

# Test Case: Both min_repetitions and max_repetitions are None
def test_both_min_max_repetitions_none():
    with pytest.raises(ValueError):
        ElementRepetitionConstraint(ElementType.WORDS, "world")

# Test Case: min_repetitions greater than max_repetitions
def test_min_repetitions_greater_than_max_repetitions():
    with pytest.raises(ValueError):
        ElementRepetitionConstraint(ElementType.CHARACTERS, "a", min_repetitions=3, max_repetitions=2)