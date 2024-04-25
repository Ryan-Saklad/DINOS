import pytest
from benchmark.problems.math_expression_problem import MathExpressionProblem

@pytest.mark.parametrize("expression, expected_result, text", [
    ("((-1 + 2 + 9 * 5) - (-2 + -4 + -4 * -7))", "24", "Sure, here you go!\n24"),
    ("((-9 * -5 - 6 + -2) - (-8 - -6 * -3 * 1))", "63", "Sure, here you go!\n63"),
    ("((3 * -3 * 6 + -5) - (-2 + -7 - 7 - -7))", "-50", "Sure, here you go!\n-50"),
    ("((6 * -6 * 8 * 1) * (-1 * 7 * -6 + -2))", "-11520", "Sure, here you go!\n-11520"),
    ("((-6 - -4 + 9 + 0) + (1 + -4 - -9 * 6))", "58", "Sure, here you go!\n58"),
    ("((-6 - 4 * 2 - 6) + (1 + -2 * 1 * 7))", "-33", "Sure, here you go!\n-33"),
    ("((1 - 0 + 1 - 4) - (-3 * 1 - -6 * -8))", "49", "Sure, here you go!\n49"),
    ("((1 + 7 * -9 + -5) + (3 + -5 * 2 - 6))", "-80", "Sure, here you go!\n-80"),
    ("((-7 * -9 + 8 * -3) * (5 + -7 - 4 * -5))", "702", "Sure, here you go!\n702"),
    ("((-9 - 1 * 5 * -5) - (6 + -3 - -1 * -7))", "20", "Sure, here you go!\n20"),
    ("((6 - 0 * 5 + -3) * (6 - -7 + -2 - -7))", "54", "Sure, here you go!\n54"),
    ("((2 - -2 + -7 * 8) * (-7 * -8 * 3 - -2))", "-8840", "Sure, here you go!\n-8840"),
    ("((8 - 2 + -2 * 6) * (8 + -6 + -8 + -1))", "42", "Sure, here you go!\n42"),
    ("((-6 + -9 - -6 + -4) * (-1 - -6 + -4 - 3))", "26", "Sure, here you go!\n26"),
    ("((-5 - 4 * -8 + 8) * (4 + 3 - 9 * 7))", "-1960", "Sure, here you go!\n-1960"),
    ("((-5 * -7 * -6 + 9) * (-2 - 8 + -5 + 7))", "1608", "Sure, here you go!\n1608"),
    ("((8 + 9 - 4 - -9) + (8 + 7 - 6 * 1))", "31", "Sure, here you go!\n31"),
    ("((5 * -1 + -6 * -3) + (-1 + -8 - 5 + 3))", "2", "Sure, here you go!\n2")
])
def test_math_expression_problem(expression, expected_result, text):
    problem = MathExpressionProblem()
    problem.problem = expression
    problem.answer = expected_result
    assert problem.validate(text) == True

@pytest.mark.parametrize("expression, expected_result, text", [
    ("((-1 + 2 + 9 * 5) - (-2 + -4 + -4 * -7))", "25", "Sure, here you go!\n25"),
    ("((-9 * -5 - 6 + -2) - (-8 - -6 * -3 * 1))", "64", "Sure, here you go!\n64"),
    ("((3 * -3 * 6 + -5) - (-2 + -7 - 7 - -7))", "-51", "Sure, here you go!\n-51"),
    ("((6 * -6 * 8 * 1) * (-1 * 7 * -6 + -2))", "-11521", "Sure, here you go!\n-11521"),
    ("((-6 - -4 + 9 + 0) + (1 + -4 - -9 * 6))", "59", "Sure, here you go!\n59"),
    ("((-6 - 4 * 2 - 6) + (1 + -2 * 1 * 7))", "-34", "Sure, here you go!\n-34"),
    ("((1 - 0 + 1 - 4) - (-3 * 1 - -6 * -8))", "50", "Sure, here you go!\n50"),
    ("((1 + 7 * -9 + -5) + (3 + -5 * 2 - 6))", "-81", "Sure, here you go!\n-81"),
    ("((-7 * -9 + 8 * -3) * (5 + -7 - 4 * -5))", "703", "Sure, here you go!\n703"),
    ("((-9 - 1 * 5 * -5) - (6 + -3 - -1 * -7))", "21", "Sure, here you go!\n21"),
    ("((6 - 0 * 5 + -3) * (6 - -7 + -2 - -7))", "55", "Sure, here you go!\n55"),
    ("((2 - -2 + -7 * 8) * (-7 * -8 * 3 - -2))", "-8841", "Sure, here you go!\n-8841"),
    ("((8 - 2 + -2 * 6) * (8 + -6 + -8 + -1))", "43", "Sure, here you go!\n43"),
    ("((-6 + -9 - -6 + -4) * (-1 - -6 + -4 - 3))", "27", "Sure, here you go!\n27"),
    ("((-5 - 4 * -8 + 8) * (4 + 3 - 9 * 7))", "-1961", "Sure, here you go!\n-1961"),
    ("((-5 * -7 * -6 + 9) * (-2 - 8 + -5 + 7))", "1609", "Sure, here you go!\n1609"),
    ("((8 + 9 - 4 - -9) + (8 + 7 - 6 * 1))", "32", "Sure, here you go!\n32"),
    ("((5 * -1 + -6 * -3) + (-1 + -8 - 5 + 3))", "3", "Sure, here you go!\n3"),
    ("((-1 + 2 + 9 * 5) - (-2 + -4 + -4 * -7))", "", "Sure, here you go!\n"),
    ("((-9 * -5 - 6 + -2) - (-8 - -6 * -3 * 1))", "abc", "Sure, here you go!\nabc")
])
def test_math_expression_problem_incorrect(expression, expected_result, text):
    problem = MathExpressionProblem()
    problem.problem = expression
    problem.answer = str(eval(expression))
    assert problem.validate(text) == False