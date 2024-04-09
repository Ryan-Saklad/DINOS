import pytest

from benchmark.problems.boolean_expression_problem import BooleanExpressionProblem

@pytest.mark.parametrize("expression, expected_result", [
    ("not ( True ) and ( True )", "False"),
    ("True and not not ( not False )", "True"),
    ("not True or False or ( False )", "False"),
    ("False or not ( True ) and False", "False"),
    ("True or not False and True and False", "True"),
    ("False or not not not False and True", "True"),
    ("not True and ( False or True )", "False"),
    ("True and not False or ( True )", "True"),
    ("not True or ( False and True )", "False"),
    ("not True or ( True or False )", "True"),
    ("False or ( False ) and not False", "False"),
    ("not False or True and False and False", "True"),
    ("not True or False or not not True", "True"),
    ("True and True and False and not True", "False"),
    ("not not True and not True or True", "True"),
    ("not not not ( True and False )", "True"),
    ("not not False and not not not False", "False")
])
def test_boolean_expression_problem(expression, expected_result):
    problem = BooleanExpressionProblem()
    problem.problem = expression
    problem.answer = expected_result
    assert problem.validate(expected_result) == True

@pytest.mark.parametrize("expression, expected_result", [
    ("not ( True ) and ( True )", "True"),
    ("True and not not ( not False )", "False"),
    ("not True or False or ( False )", "True"),
    ("False or not ( True ) and False", "True"),
    ("True or not False and True and False", "False"),
    ("False or not not not False and True", "False"),
    ("not True and ( False or True )", "True"),
    ("True and not False or ( True )", "False"),
    ("not True or ( False and True )", "True"),
    ("not True or ( True or False )", "False"),
    ("False or ( False ) and not False", "True"),
    ("not False or True and False and False", "False"),
    ("not True or False or not not True", "False"),
    ("True and True and False and not True", "True"),
    ("not not True and not True or True", "False"),
    ("not not not ( True and False )", "False"),
    ("not not False and not not not False", "True"),
    ("not not False and not not not False", ""),
    ("not not False and not not not False", "true"),
    ("not not False and not not not False", "false")
])
def test_boolean_expression_problem(expression, expected_result):
    problem = BooleanExpressionProblem()
    problem.problem = expression
    problem.answer = BooleanExpressionProblem().evaluate(expression)
    assert problem.validate(expected_result) == False