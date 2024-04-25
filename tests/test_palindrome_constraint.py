import pytest
from benchmark.constraints.palindrome_constraint import PalindromeConstraint

@pytest.mark.parametrize("response, expected_result", [
    ("Sure, here you go!\nracecar", True),
    ("Sure, here you go!\nhello", False),
    ("Sure, here you go!\nA man, a plan, a canal, Panama", True),
    ("Sure, here you go!\nWas it a car or a cat I saw?", True),
    ("Sure, here you go!\nNo lemon, no melon", True)
])
def test_palindrome_constraint(response: str, expected_result: bool):
    constraint = PalindromeConstraint()
    assert constraint.validate(response) == expected_result

def test_palindrome_constraint_empty_string():
    constraint = PalindromeConstraint()
    assert constraint.validate("")
