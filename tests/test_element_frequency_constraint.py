import pytest

from benchmark.constraints.element_frequency_constraint import ElementFrequencyConstraint
from utils.element_type import ElementType

# Test Cases
@pytest.mark.parametrize("text, element_type, element, min_frequency, max_frequency, case_sensitive, expected", [
   # Test case for case-insensitive character frequency within range
   ("Hello", ElementType.CHARACTERS, "l", 0.3, 0.5, False, True),
   # Test case for case-sensitive character frequency within range
   ("Hello", ElementType.CHARACTERS, "L", 0.2, 0.4, True, False),
   # Test case for case-insensitive word frequency above minimum
   ("OpenAI ChatGPT", ElementType.WORDS, "chatgpt", 0.1, None, False, True),
   # Test case for case-sensitive word frequency above minimum
   ("OpenAI ChatGPT", ElementType.WORDS, "ChatGPT", 0.1, None, True, True),
   # Test case for case-insensitive character frequency below maximum
   ("Anthropic", ElementType.CHARACTERS, "i", None, 0.2, False, True),
   # Test case for case-sensitive character frequency below maximum
   ("Anthropic", ElementType.CHARACTERS, "I", None, 0.2, True, True),
   # Test case for case-insensitive word frequency outside the range
   ("Claude", ElementType.WORDS, "claude", 0.6, 0.8, False, False),
   # Test case for case-sensitive word frequency outside the range
   ("Claude", ElementType.WORDS, "Claude", 0.6, 0.8, True, False),
])
def test_element_frequency(text, element_type, element, min_frequency, max_frequency, case_sensitive, expected):
   constraint = ElementFrequencyConstraint(element_type, element, min_frequency, max_frequency, case_sensitive)
   assert constraint.validate(text) == expected

# Test Case for Invalid Element Input
def test_invalid_element():
   with pytest.raises(ValueError):
       ElementFrequencyConstraint(ElementType.CHARACTERS, "")

# Test Case for min_frequency > max_frequency
def test_invalid_frequency():
   with pytest.raises(ValueError):
       ElementFrequencyConstraint(ElementType.WORDS, "hello", min_frequency=0.6, max_frequency=0.4)

# Test Case for Unsupported Element Type
def test_unsupported_element_type():
   with pytest.raises(ValueError):
       ElementFrequencyConstraint("InvalidType", "element")

# Test Case for No Frequency Specified
def test_no_frequency_specified():
   with pytest.raises(ValueError):
       ElementFrequencyConstraint(ElementType.CHARACTERS, "a")

# Test Case for Case-Sensitive Character Frequency
def test_case_sensitive_character_frequency():
   constraint = ElementFrequencyConstraint(ElementType.CHARACTERS, "A", min_frequency=0.1, max_frequency=0.3, case_sensitive=True)
   assert constraint.validate("Anthropic AI") == True
   assert constraint.validate("anthropic ai") == False

# Test Case for Case-Insensitive Word Frequency
def test_case_insensitive_word_frequency():
   constraint = ElementFrequencyConstraint(ElementType.WORDS, "openai", min_frequency=0.2, max_frequency=0.4, case_sensitive=False)
   assert constraint.validate("OpenAI is an AI company") == True
   assert constraint.validate("Openai Is An Ai Company") == True
