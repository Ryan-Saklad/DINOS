import pytest
from benchmark.constraints.write_backwards_constraint import WriteBackwardsConstraint

@pytest.mark.parametrize("original_text, response, expected_result", [
    ("hello", "olleh", True),
    ("world", "dlrow", True),
    ("python", "nohtyp", True),
    ("test", "tset", True),
    ("example", "elpmaxe", True),
    ("12345", "54321", True),
    ("", "", True),
    ("hello", "hello", False),
    ("world", "world", False),
    ("python", "python", False)
])
def test_write_backwards_constraint(original_text: str, response: str, expected_result: bool):
    constraint = WriteBackwardsConstraint()
    assert constraint.validate(response, original_text) == expected_result
