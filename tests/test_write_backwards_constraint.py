import pytest
from benchmark.constraints.write_backwards_constraint import WriteBackwardsConstraint

@pytest.mark.parametrize("original_text, response, expected_result", [
    ("hello", "Sure, here you go!\nolleh", True),
    ("world", "Sure, here you go!\ndlrow", True),
    ("python", "Sure, here you go!\nnohtyp", True),
    ("test", "Sure, here you go!\ntset", True),
    ("example", "Sure, here you go!\nelpmaxe", True),
    ("12345", "Sure, here you go!\n54321", True),
    ("", "Sure, here you go!\n", True),
    ("hello", "Sure, here you go!\nhello", False),
    ("world", "Sure, here you go!\nworld", False),
    ("python", "Sure, here you go!\npython", False)
])
def test_write_backwards_constraint(original_text: str, response: str, expected_result: bool):
    constraint = WriteBackwardsConstraint()
    assert constraint.validate(response, original_text) == expected_result
