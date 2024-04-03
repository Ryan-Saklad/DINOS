import datetime
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
    ("hello: world: foo", False),  # must be a key: value pair
    ("hello: world", True),
    ("hello:\n\t- foo\n\t- bar", False),  # can't use tabs as whitespace
    ("hello:\n- foo\n- bar", True),
    ("1: hello", True),
    ("hello: [foo, bar, 2.0, 3e10, 0xC, 0o14]\nworld:\n  - leggo\n  - myeggo", True),  # additional data types
    (f"hello: {datetime.datetime.now()}", True)
])
def test_yaml(text, expected):
    constraint = OutputFormatConstraint(OutputType.YAML)
    assert constraint.validate(text) == expected

    # confirm correct violation is recorded
    if not expected:
        assert len(constraint.violations) == 1
        assert constraint.violations[0] == "The response is not in yaml format."


xml_text_1 = """<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</note>
"""
xml_text_2 = """
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
</note>
<body>Don't forget me this weekend!</body>
"""
xml_text_3 = """
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</note>
<?xml version="1.0" encoding="UTF-8"?>"""
xml_text_4 = """
<p>This is a paragraph.</p>
<br />"""
xml_text_5 = "<message>This is correct</Message>"
xml_text_6 = "<b><i>This text is bold and italic</b></i>"
xml_text_7 = "<b><i>This text is bold and italic</i></b>"
xml_text_8 = """
<note date=12/11/2007>
  <to>Tove</to>
  <from>Jani</from>
</note>"""
xml_text_9 = """
<note date="12/11/2007">
  <to>Tove</to>
  <from>Jani</from>
</note>"""
xml_text_10 = """<message>salary < 1000</message>"""
xml_text_11 = """<message>salary &lt; 1000</message>"""


@pytest.mark.parametrize("text, expected", [
    (xml_text_1, True),
    (xml_text_2, False),  # all elements must have a root
    (xml_text_3, False),  # prolog must come first if it exists
    (xml_text_4, False),  # elements must have a closing tag
    (xml_text_5, False),  # tags are case-sensitive
    (xml_text_6, False),  # tags must be nested properly
    (xml_text_7, True),
    (xml_text_8, False),  # attribute values must be quoted
    (xml_text_9, True),
    (xml_text_10, False),  # entity references are required for special characters
    (xml_text_11, True),
])
def test_xml(text, expected):
    constraint = OutputFormatConstraint(OutputType.XML)
    assert constraint.validate(text) == expected

    # confirm correct violation is recorded
    if not expected:
        assert len(constraint.violations) == 1
        assert constraint.violations[0] == "The response is not in xml format."
