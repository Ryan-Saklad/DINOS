import pytest
from benchmark.constraints.palindrome_constraint import PalindromeConstraint

@pytest.mark.parametrize("response, expected_result", [
    ("racecar", True),
    ("hello", False),
    ("A man, a plan, a canal, Panama", True),
    ("Was it a car or a cat I saw?", True),
    ("No lemon, no melon", True)
])
def test_palindrome_constraint(response: str, expected_result: bool):
    constraint = PalindromeConstraint()
    assert constraint.validate(response) == expected_result

def test_palindrome_constraint_empty_string():
    constraint = PalindromeConstraint()
    assert constraint.validate("")
