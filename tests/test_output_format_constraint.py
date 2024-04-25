import datetime
import pytest

from benchmark.constraints.output_format_constraint import OutputFormatConstraint
from utils.output_type import OutputType


@pytest.mark.parametrize("text, expected, response", [
    ('Sure, here you go!\n{ "Response": "world" }', True, 'world'),  # key/value must be in double quotes
    ('Sure, here you go!\n{ "hello": "world" }', False, None),  # the response must be given with a 'Response' key
    ("Sure, here you go!\n{ hello: world }", False, None),
    ('Sure, here you go!\n{ 1: "world" }', False, None),  # key must be a string
    ('Sure, here you go!\n{ true: "world" }', False, None),
    ('Sure, here you go!\n{ false: "world" }', False, None),
    ('Sure, here you go!\n{ null: "world" }', False, None),
    ('Sure, here you go!\n{ 1.0: "world" }', False, None),
    ('Sure, here you go!\n{ "Response": 1 }', True, 1),  # values can be numbers
    ('Sure, here you go!\n{ "Response": 1.0 }', True, 1.0),
    ('Sure, here you go!\n{ "Response": 2e10 }', True, 2e10),
    ('Sure, here you go!\n{ "Response": 2E-10 }', True, 2E-10),
    ('Sure, here you go!\n{ "Response": { "foo": "bar" } }', True, dict(foo='bar')),  # values can be nested objects
    ('Sure, here you go!\n{ "hello": { 1: "bar" } }', False, None),
    ('Sure, here you go!\n{ "Response": ["world", "foo", "bar"] }', True, ['world', 'foo', 'bar']),  # values can be arrays
    ('Sure, here you go!\n{ "Response": [1, 2, 3, 4] }', True, [1, 2, 3, 4]),
    ('Sure, here you go!\n{ "Response": [true, false, true, false] }', True, [True, False, True, False]),
    ('Sure, here you go!\n{ "Response": [null, null, true, false] }', True, [None, None, True, False]),
    ('Sure, here you go!\n{ "Response": ["world", 1, true, null] }', True, ['world', 1, True, None]),  # mixed-type arrays are allowed in json
    ('Sure, here you go!\n{ "Response": [{"foo": "bar", "yes": "no"}, { "mr": "mrs" }] }', True, [dict(foo='bar', yes='no'), dict(mr='mrs')]),
    ('Sure, here you go!\n{"Response":"world"}', True, 'world'),  # whitespace doesn't matter
    ('Sure, here you go!\n  {  "Response"  :  "world"  }  ', True, 'world'),
    ('Sure, here you go!\n\t{\t"Response"\t:\t"world"\t}\t', True, 'world'),
    ('Sure, here you go!\n\n{\n"Response"\n:\n"world"\n}\n', True, 'world'),
    ('Sure, here you go!\n\n\r{\n\r"Response"\n\r:\n\r"world"\n\r}\n\r', True, 'world'),
])
def test_json(text, expected, response):
    constraint = OutputFormatConstraint(OutputType.JSON)
    assert constraint.validate(text) == expected
    assert constraint.response == response

    # confirm correct violation is recorded
    if not expected:
        assert len(constraint.violations) == 1
        assert constraint.violations[0] == "The response is not in the requested format."


@pytest.mark.parametrize("text, expected, response", [
    ("Sure, here you go!\nhello: world: foo", False, None),  # must be a key: value pair
    ("Sure, here you go!\nResponse: world", True, 'world'),
    ("Sure, here you go!\nhello:\n\t- foo\n\t- bar", False, None),  # can't use tabs as whitespace
    ("Sure, here you go!\nResponse:\n- foo\n- bar", True, ['foo', 'bar']),
    ("Sure, here you go!\n1: hello", False, None),
    ("Sure, here you go!\nResponse: [foo, bar, 2.0, 0xC]\nworld:\n  - leggo\n  - myeggo", True, ['foo', 'bar', 2.0, 0xC]),  # additional data types
])
def test_yaml(text, expected, response):
    constraint = OutputFormatConstraint(OutputType.YAML)
    assert constraint.validate(text) == expected
    assert constraint.response == response

    # confirm correct violation is recorded
    if not expected:
        assert len(constraint.violations) == 1
        assert constraint.violations[0] == "The response is not in the requested format."


xml_text_1 = """Sure, here you go!\n<?xml version="1.0" encoding="UTF-8"?>
<Response>
  This is the response
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</Response>
"""
xml_text_2 = """Sure, here you go!\n
<Response>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
</Response>
<body>Don't forget me this weekend!</body>
"""
xml_text_3 = """Sure, here you go!\n
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</note>
<?xml version="1.0" encoding="UTF-8"?>"""
xml_text_4 = """Sure, here you go!\n
<p>This is a paragraph.</p>
<br />"""
xml_text_5 = "Sure, here you go!\n<message>This is correct</Message>"
xml_text_6 = "Sure, here you go!\n<b><i>This text is bold and italic</b></i>"
xml_text_7 = "Sure, here you go!\n<response><i>This text is bold and italic</i></response>"
xml_text_8 = """Sure, here you go!\n
<note date=12/11/2007>
  <to>Tove</to>
  <from>Jani</from>
</note>"""
xml_text_9 = """Sure, here you go!\n
<response date="12/11/2007">
  <to>Tove</to>
  response
  <from>Jani</from>
</response>"""
xml_text_10 = """Sure, here you go!\n<message>salary < 1000</message>"""
xml_text_11 = """Sure, here you go!\n<Response>salary &lt; 1000</Response>"""


@pytest.mark.parametrize("text, expected, response", [
    (xml_text_1, True, 'This is the response'),
    (xml_text_2, False, None),  # all elements must have a root
    (xml_text_3, False, None),  # prolog must come first if it exists
    (xml_text_4, False, None),  # elements must have a closing tag
    (xml_text_5, False, None),  # tags are case-sensitive
    (xml_text_6, False, None),  # tags must be nested properly
    (xml_text_7, False, None),
    (xml_text_8, False, None),  # attribute values must be quoted
    (xml_text_9, True, ''),
    (xml_text_10, False, None),  # entity references are required for special characters
    (xml_text_11, True, 'salary < 1000'),
])
def test_xml(text, expected, response):
    constraint = OutputFormatConstraint(OutputType.XML)
    assert constraint.validate(text) == expected
    assert constraint.response == response

    # confirm correct violation is recorded
    if not expected:
        assert len(constraint.violations) == 1
        assert constraint.violations[0] == "The response is not in the requested format."


# wrap_1 = "###"
# wrap_2 = "$$"
# wrap_3 = "@"
# wrap_4 = "------"
# wrap_5 = "@#$%"
# wrap_6 = "%$#"
# wrap_text_1 = f"""{wrap_1}
# hello
# world
# {wrap_1}"""
# wrap_text_2 = f"""Sure, thing. Here's my response
#
# {wrap_2}
# leggo
# my
# eggo
# {wrap_2}"""
# wrap_text_3 = f"""{wrap_3}foo bar
# baz
# 1234329487{wrap_3}"""
# wrap_text_4 = f"""
# {wrap_4}
# this
# shouldn't
# matter
# """
# wrap_text_5 = f"""
# cuckoo
# for
# cocoa
# puffs
# {wrap_5}
# """
# wrap_text_6 = f"""-{wrap_6}
# this
# should
# fail
# {wrap_6}-"""
#
#
# @pytest.mark.parametrize("text, wrap_text, wrap_lines, expected, response", [
#     (wrap_text_1, wrap_1, 3, True, '\nhello\nworld\n'),
#     (wrap_text_2, wrap_2, 3, True, 'Sure, thing. Here\'s my response\n\n\nleggo\nmy\neggo\n'),
#     (wrap_text_2, wrap_2, 2, False, None),  # wrap_lines is too small
#     (wrap_text_3, wrap_3, 3, True, 'foo bar\nbaz\n1234329487'),
#     (wrap_text_4, wrap_4, 2, False, None),  # wrap text only at start
#     (wrap_text_5, wrap_5, 1, False, None),  # wrap text only at end
#     (wrap_text_6, wrap_6, 2, False, None)
# ])
# def test_wrap(text, wrap_text, wrap_lines, expected, response):
#     constraint = OutputFormatConstraint(OutputType.WRAP, wrap_text, wrap_lines)
#     assert constraint.validate(text) == expected
#     assert constraint.response == response
#
#     # confirm correct violation is recorded
#     if not expected:
#         assert len(constraint.violations) == 1
#         assert constraint.violations[0] == "The response is not in the requested format."


def test_exceptions():
    with pytest.raises(ValueError):
        OutputFormatConstraint(OutputType.WRAP, "")
        OutputFormatConstraint("test")


@pytest.mark.parametrize("output_type, wrap_text, expected", [
    (OutputType.JSON, "", "The response must be given in JSON format. There should be a 'Response' key with corresponding value equal to the response."),
    (OutputType.YAML, "", "The response must be given in YAML format. There should be a 'Response' key with corresponding value equal to the response."),
    (OutputType.XML, "", "The response must be given in XML format. The root tag should be named 'Response' and should directly enclose the response."),
    # (OutputType.WRAP, "####", "The response must be enclosed in '####' characters. That is, the response should start and end with '####'.")
])
def test_description_text(output_type, wrap_text, expected):
    constraint = OutputFormatConstraint(output_type, wrap_text)
    assert constraint.description == expected
