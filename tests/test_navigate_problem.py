import pytest
from benchmark.problems.navigate_problem import NavigateProblem

@pytest.mark.parametrize("num_steps, min_distance, max_distance, manual_answer, text, expected_result", [
    (3, 1, 5, "(-4, -2)", "Sure, here you go!\n(-4, -2)", True),
    (5, 2, 8, "(12, -10)", "Sure, here you go!\n(12, -10)", True),
    (2, 3, 7, "(4, 7)", "Sure, here you go!\n(4, 7)", True),
    (4, 1, 10, "(-5, 8)", "Sure, here you go!\n(-5, 8)", True)
])
def test_navigate_problem(num_steps: int, min_distance: int, max_distance: int, manual_answer: str, text: str, expected_result: bool):
    problem = NavigateProblem()
    problem.generate(num_steps, min_distance, max_distance)
    problem.answer = manual_answer  # Manually setting the answer for validation
    assert problem.validate(text) == expected_result

def test_navigate_problem_incorrect_answer():
    problem = NavigateProblem()
    problem.generate(4, 2, 6)
    assert not problem.validate("Sure, here you go!\n(1, 2, 3)")

def test_navigate_problem_case_insensitive():
    problem = NavigateProblem()
    problem.generate(3, 1, 5)
    assert problem.validate('Sure, here you go!\n' + problem.answer.upper())
    assert problem.validate('Sure, here you go!\n' + problem.answer.lower())
