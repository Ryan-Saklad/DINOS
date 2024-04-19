import pytest
from benchmark.problems.dyck_language_problem import DyckLanguageProblem

@pytest.mark.parametrize("problem_input, expected_result", [
    ("[ [", "] ]"),
    ("< [ [", "] ] >"),
    ('{ < { { [ ] } } { < [ { { < > } } [ ( ) ( ) ] [ [ [ [ ( { < ( < ( [ ] ) > ) > } ) ] ] ] ] ] ] ( ) ( [ ] { } ) > } > [ { ( ( ) ) } ]', "}"),
    ("< [ ] { < ( ) > } [ ] ( { }", ") >"),
    ("< ( ( ( < > ) ) ( { { } [ { } ] [ ] < ( ) > } ) )", ">"),
    ("( [ [ [ { } ] ] { < [ < [ { } ] > ] > }", "] )"),
    ("( { { } }", ")"),
    ("< ( ( ( [ { } ] )", ") ) >"),
    ("[ < > ] [ [ < > ]", "]"),
    ("[ ] ( [ [ { < { { ( < > [ ] ) } } < > > } ] ] { }", ")"),
    ("[ < [ ] ( ) ( ( { { } } ) ) < { < > } > [ ] > ] < ( ) > ( ( ( ) ) ) ( < >", ")"),
    ("[ { < ( ) > }", "]"),
    ('[ < [ ( ( ) < ( ) > ( { { } } [ [ [ < ( [ ] ) ( ) > ] ] ] { { { { { } } } { { } { < [ [ ] ] > } } { } } } ) ) ] >', "]"),
    ('< ( ( [ < > { [ { ( ) } ] < { < { } > [ ( < > ) ] } > } [ < > ] ] ) { { ( { ( ( [ ( [ ] ) ] < { } > ) ) { { ( [ [ ] ] ) } [ ( ) ] { { [ ] } } } } ) } ( { } ) }', ") >"),
    ("[ ] { ( ( < { ( ( ( { < > ( ) } ) ) [ { } ] { { ( ) } } ) } < > >", ") ) }"),
    ("< { < > } { (", ") } >"),
    ("[ [ < < { } >", "> ] ]"),
    ("< ( ( )", ") >"),
    ("( ( ) ) [ { ( < > ) }", "]"),
])
def test_dyck_languages_problem(problem_input, expected_result):
    problem = DyckLanguageProblem()
    problem.problem = problem_input
    problem.answer = expected_result
    assert problem.validate(expected_result) == True

@pytest.mark.parametrize("problem_input, expected_result", [
    (False, True),
    ("[ [", "] ] >"),  # Extra closing bracket
    ("< [ [", "] ]"),  # Missing closing angle bracket
    ("{ < { { [ ] } } { < [ { { < > } } [ ( ) ( ) ] [ [ [ [ ( { < ( < ( [ ] ) > ) > } ) ] ] ] ] ] ] ( ) ( [ ] { } ) > } > [ { ( ( ) ) } ]", "} >"),  # Extra closing angle bracket
    ("< [ ] { < ( ) > } [ ] ( { }", ") > )"),  # Extra closing parenthesis
    ("< ( ( ( < > ) ) ( { { } [ { } ] [ ] < ( ) > } ) )", ""),  # Missing closing angle bracket
    ("( [ [ [ { } ] ] { < [ < [ { } ] > ] > }", "] ] )"),  # Extra closing bracket
    ("( { { } }", "] )"),  # Wrong closing bracket
    ("< ( ( ( [ { } ] )", ") ) ) >"),  # Extra closing parenthesis
    ("[ < > ] [ [ < > ]", "] >"),  # Extra closing angle bracket
    ("[ ] ( [ [ { < { { ( < > [ ] ) } } < > > } ] ] { }", "] )"),  # Wrong closing bracket
    ])
def test_dyck_languages_problem_f(problem_input, expected_result):
    problem = DyckLanguageProblem()
    problem.problem = problem_input
    problem.answer = expected_result
    assert problem.validate(problem_input) == False