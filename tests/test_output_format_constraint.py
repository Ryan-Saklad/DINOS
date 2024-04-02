import pytest

from benchmark.constraints.output_format_constraint import OutputFormatConstraint
from utils.output_type import OutputType


@pytest.mark.parametrize("text, expected", [
    ('{ "hello": "world" }', True),  # key/value must be in double quotes
    ("{ hello: world }", False),
    ('{ 1: "world" }', False),  # key must be a string
    ('{ true: "world" }', False),
    ('{ false: "world" }', False),
    ('{ null: "world" }', False),
    ('{ "1": "world" }', True),
    ('{ 1.0: "world" }', False),
    ('{ "hello": 1 }', True),  # values can be numbers
    ('{ "hello": 1.0 }', True),
    ('{ "hello": 2e10 }', True),
    ('{ "hello": 2E-10 }', True),
    ('{ "hello": { "foo": "bar" } }', True),  # values can be nested objects
    ('{ "hello": { 1: "bar" } }', False),
    ('{ "hello": ["world", "foo", "bar"] }', True),  # values can be arrays
    ('{ "hello": [1, 2, 3, 4] }', True),
    ('{ "hello": [true, false, true, false] }', True),
    ('{ "hello": [null, null, true, false] }', True),
    ('{ "hello": ["world", 1, true, null] }', True),  # mixed-type arrays are allowed in json
    ('{ "hello": [{"foo": "bar", "yes": "no"}, { "mr": "mrs" }] }', True),
    ('{"hello":"world"}', True),  # whitespace doesn't matter
    ('  {  "hello"  :  "world"  }  ', True),
    ('\t{\t"hello"\t:\t"world"\t}\t', True),
    ('\n{\n"hello"\n:\n"world"\n}\n', True),
    ('\n\r{\n\r"hello"\n\r:\n\r"world"\n\r}\n\r', True),
])
def test_json(text, expected):
    constraint = OutputFormatConstraint(OutputType.JSON)
    assert constraint.validate(text) == expected

    # confirm correct violation is recorded
    if not expected:
        assert len(constraint.violations) == 1
        assert constraint.violations[0] == "The response is not in json format."


@pytest.mark.parametrize("text, expected", [
    ('{ "hello": "world" }', False),
])
def test_yaml(text, expected):
    constraint = OutputFormatConstraint(OutputType.YAML)
    assert constraint.validate(text) == expected

    # confirm correct violation is recorded
    if not expected:
        assert len(constraint.violations) == 1
        assert constraint.violations[0] == "The response is not in yaml format."
