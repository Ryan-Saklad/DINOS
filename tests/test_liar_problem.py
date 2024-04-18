import pytest

from benchmark.problems.liar_problem import LiarProblem

@pytest.mark.parametrize("names, truthfulness_list, expected_result", [
    (["Maria", "Nushi", "Mohammed", "Jose", "Muhammad"], [True, False, True, False, True], True),
    (["Wei", "Mohammad", "Ahmed"], [False, True, False], False),
    (["Yan", "Ali", "John"], [True, False, True], True),
    (["David", "Li", "Abdul", "Ana"], [False, True, False, True], True)
])
def test_liar_problem(names: list[str], truthfulness_list: list[bool], expected_result: bool):
    problem = LiarProblem()
    problem.names = names
    problem.truthfulness = dict(zip(names, truthfulness_list))
    last_person_name = names[-1]
    assert problem.validate(str(problem.truthfulness[last_person_name]))
