import pytest

from benchmark.problems.boolean_expression_problem import BooleanExpressionProblem

@pytest.mark.parametrize("expression, expected_result", [
    ("not ( True ) and ( True )", "Sure, here you go!\nFalse"),
    ("True and not not ( not False )", "Sure, here you go!\nTrue"),
    ("not True or False or ( False )", "Sure, here you go!\nFalse"),
    ("False or not ( True ) and False", "Sure, here you go!\nFalse"),
    ("True or not False and True and False", "Sure, here you go!\nTrue"),
    ("False or not not not False and True", "Sure, here you go!\nTrue"),
    ("not True and ( False or True )", "Sure, here you go!\nFalse"),
    ("True and not False or ( True )", "Sure, here you go!\nTrue"),
    ("not True or ( False and True )", "Sure, here you go!\nFalse"),
    ("not True or ( True or False )", "Sure, here you go!\nTrue"),
    ("False or ( False ) and not False", "Sure, here you go!\nFalse"),
    ("not False or True and False and False", "Sure, here you go!\nTrue"),
    ("not True or False or not not True", "Sure, here you go!\nTrue"),
    ("True and True and False and not True", "Sure, here you go!\nFalse"),
    ("not not True and not True or True", "Sure, here you go!\nTrue"),
    ("not not not ( True and False )", "Sure, here you go!\nTrue"),
    ("not not False and not not not False", "Sure, here you go!\nFalse")
])
def test_boolean_expression_problem(expression, expected_result):
    problem = BooleanExpressionProblem()
    problem.problem = expression
    problem.answer = expected_result
    assert problem.validate(expected_result) == True

@pytest.mark.parametrize("expression, expected_result", [
    ("not ( True ) and ( True )", "Sure, here you go!\nTrue"),
    ("True and not not ( not False )", "Sure, here you go!\nFalse"),
    ("not True or False or ( False )", "Sure, here you go!\nTrue"),
    ("False or not ( True ) and False", "Sure, here you go!\nTrue"),
    ("True or not False and True and False", "Sure, here you go!\nFalse"),
    ("False or not not not False and True", "Sure, here you go!\nFalse"),
    ("not True and ( False or True )", "Sure, here you go!\nTrue"),
    ("True and not False or ( True )", "Sure, here you go!\nFalse"),
    ("not True or ( False and True )", "Sure, here you go!\nTrue"),
    ("not True or ( True or False )", "Sure, here you go!\nFalse"),
    ("False or ( False ) and not False", "Sure, here you go!\nTrue"),
    ("not False or True and False and False", "Sure, here you go!\nFalse"),
    ("not True or False or not not True", "Sure, here you go!\nFalse"),
    ("True and True and False and not True", "Sure, here you go!\nTrue"),
    ("not not True and not True or True", "Sure, here you go!\nFalse"),
    ("not not not ( True and False )", "Sure, here you go!\nFalse"),
    ("not not False and not not not False", "Sure, here you go!\nTrue"),
    ("not not False and not not not False", "Sure, here you go!\n"),
    ("not not False and not not not False", "Sure, here you go!\ntrue"),
    ("not not False and not not not False", "Sure, here you go!\nfalse")
])
def test_boolean_expression_problem(expression, expected_result):
    problem = BooleanExpressionProblem()
    problem.problem = expression
    problem.answer = BooleanExpressionProblem().evaluate(expression)
    assert problem.validate(expected_result) == False