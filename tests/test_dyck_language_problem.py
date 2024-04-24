import pytest
from benchmark.problems.dyck_language_problem import DyckLanguageProblem

@pytest.mark.parametrize("problem_input, expected_result, text", [
    ("[ [", "] ]", "Sure, here you go!\n] ]"),
    ("< [ [", "] ] >", "Sure, here you go!\n] ] >"),
    ('{ < { { [ ] } } { < [ { { < > } } [ ( ) ( ) ] [ [ [ [ ( { < ( < ( [ ] ) > ) > } ) ] ] ] ] ] ] ( ) ( [ ] { } ) > } > [ { ( ( ) ) } ]', "}", "Sure, here you go!\n}"),
    ("< [ ] { < ( ) > } [ ] ( { }", ") >", "Sure, here you go!\n) >"),
    ("< ( ( ( < > ) ) ( { { } [ { } ] [ ] < ( ) > } ) )", ">", "Sure, here you go!\n>"),
    ("( [ [ [ { } ] ] { < [ < [ { } ] > ] > }", "] )", "Sure, here you go!\n] )"),
    ("( { { } }", ")", "Sure, here you go!\n)"),
    ("< ( ( ( [ { } ] )", ") ) >", "Sure, here you go!\n) ) >"),
    ("[ < > ] [ [ < > ]", "]", "Sure, here you go!\n]"),
    ("[ ] ( [ [ { < { { ( < > [ ] ) } } < > > } ] ] { }", ")", "Sure, here you go!\n)"),
    ("[ < [ ] ( ) ( ( { { } } ) ) < { < > } > [ ] > ] < ( ) > ( ( ( ) ) ) ( < >", ")", "Sure, here you go!\n)"),
    ("[ { < ( ) > }", "]", "Sure, here you go!\n]"),
    ('[ < [ ( ( ) < ( ) > ( { { } } [ [ [ < ( [ ] ) ( ) > ] ] ] { { { { { } } } { { } { < [ [ ] ] > } } { } } } ) ) ] >', "]", "Sure, here you go!\n]"),
    ('< ( ( [ < > { [ { ( ) } ] < { < { } > [ ( < > ) ] } > } [ < > ] ] ) { { ( { ( ( [ ( [ ] ) ] < { } > ) ) { { ( [ [ ] ] ) } [ ( ) ] { { [ ] } } } } ) } ( { } ) }', ") >", "Sure, here you go!\n) >"),
    ("[ ] { ( ( < { ( ( ( { < > ( ) } ) ) [ { } ] { { ( ) } } ) } < > >", ") ) }", "Sure, here you go!\n) ) }"),
    ("< { < > } { (", ") } >", "Sure, here you go!\n) } >"),
    ("[ [ < < { } >", "> ] ]", "Sure, here you go!\n> ] ]"),
    ("< ( ( )", ") >", "Sure, here you go!\n) >"),
    ("( ( ) ) [ { ( < > ) }", "]", "Sure, here you go!\n]"),
])
def test_dyck_languages_problem(problem_input, expected_result, text):
    problem = DyckLanguageProblem()
    problem.problem = problem_input
    problem.answer = expected_result
    assert problem.validate(text) == True

@pytest.mark.parametrize("problem_input, text, expected_result", [
    ("False", "Sure, here you go!\nFalse", "True"),
    ("[ [", "Sure, here you go!\n[ [", "] ] >"),  # Extra closing bracket
    ("< [ [", "Sure, here you go!\n< [ [", "] ]"),  # Missing closing angle bracket
    ("{ < { { [ ] } } { < [ { { < > } } [ ( ) ( ) ] [ [ [ [ ( { < ( < ( [ ] ) > ) > } ) ] ] ] ] ] ] ( ) ( [ ] { } ) > } > [ { ( ( ) ) } ]",
     "Sure, here you go!\n{ < { { [ ] } } { < [ { { < > } } [ ( ) ( ) ] [ [ [ [ ( { < ( < ( [ ] ) > ) > } ) ] ] ] ] ] ] ( ) ( [ ] { } ) > } > [ { ( ( ) ) } ]",
     "} >"),  # Extra closing angle bracket
    ("< [ ] { < ( ) > } [ ] ( { }", "Sure, here you go!\n< [ ] { < ( ) > } [ ] ( { }", ") > )"),  # Extra closing parenthesis
    ("< ( ( ( < > ) ) ( { { } [ { } ] [ ] < ( ) > } ) )", "Sure, here you go!\n< ( ( ( < > ) ) ( { { } [ { } ] [ ] < ( ) > } ) )", ""),  # Missing closing angle bracket
    ("( [ [ [ { } ] ] { < [ < [ { } ] > ] > }", "Sure, here you go!\n( [ [ [ { } ] ] { < [ < [ { } ] > ] > }", "] ] )"),  # Extra closing bracket
    ("( { { } }", "Sure, here you go!\n( { { } }", "] )"),  # Wrong closing bracket
    ("< ( ( ( [ { } ] )", "Sure, here you go!\n< ( ( ( [ { } ] )", ") ) ) >"),  # Extra closing parenthesis
    ("[ < > ] [ [ < > ]", "Sure, here you go!\n[ < > ] [ [ < > ]", "] >"),  # Extra closing angle bracket
    ("[ ] ( [ [ { < { { ( < > [ ] ) } } < > > } ] ] { }", "Sure, here you go!\n[ ] ( [ [ { < { { ( < > [ ] ) } } < > > } ] ] { }", "] )"),  # Wrong closing bracket
    ])
def test_dyck_languages_problem_f(problem_input, text, expected_result):
    problem = DyckLanguageProblem()
    problem.problem = problem_input
    problem.answer = expected_result
    assert problem.validate(text) == False