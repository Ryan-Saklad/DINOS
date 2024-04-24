import json
import yaml
import xml.etree.ElementTree as ET

from benchmark.constraints.constraint import Constraint
from utils.output_type import OutputType
from utils.problem_type import ProblemType

class OutputFormatConstraint(Constraint):
    problem_type = ProblemType.OUTPUT_FORMAT
    def __init__(self, output_type: OutputType, wrap_text: str = "", wrap_lines: int = 3):
        """
        Initializes the output format type constraint.

        Args:
            output_type (OutputType): Specifies the output format expected in validation (e.g., json, yaml).
            wrap_text (str | None): The text to wrap output in (e.g., ###, $$$).
            wrap_lines (int): The number of lines to check for wrapping text. Defaults to 3 to ignore boilerplate
                responses and system tokens. A higher value will trade off false negatives for false positives.
            response (str | None): The model's response to a prompt that has an output format constraint. None when
                the response does not meet the requirements of the constraint.

        Raises:
            ValueError: If the provided output type is not of OutputType, or if no wrapping text is provided
                with OutputType.TEXT.
        """
        if not isinstance(output_type, OutputType):
            raise ValueError("output_type must be an instance of OutputType")
        elif output_type == OutputType.WRAP and not wrap_text:
            raise ValueError("You must provide wrapping text to use text output formatting")

        self.output_type: OutputType = output_type
        self.wrap_text: str | None = wrap_text
        self.wrap_lines: int = wrap_lines
        self.response: str | None = None
        super().__init__(self.get_description())
        self.problem_type = ProblemType.OUTPUT_FORMAT

    def validate(self, response: str, original_text: str = '') -> bool:
        """
        Validates if the given string is given in the expected output format. Upon successful validation,
        the model's response will be saved as the instance's response attribute.

        Args:
            response (str): The response text to validate.

        Returns:
            bool: True if the response matches the expected output format, False otherwise.
        """
        fmt_response = self.strip_boilerplate(response)
        match self.output_type:
            case OutputType.JSON:
                try:
                    result = json.loads(fmt_response)['Response']
                    self.response = result
                except (json.decoder.JSONDecodeError, KeyError):
                    self.violations.append("The response is not in the requested format.")
                    return False
            case OutputType.YAML:
                try:
                    result = yaml.safe_load(fmt_response)['Response']
                    self.response = result
                except (yaml.YAMLError, KeyError):
                    self.violations.append("The response is not in the requested format.")
                    return False
            case OutputType.XML:
                try:
                    result = ET.fromstring(fmt_response)
                    if result.tag.lower() != 'response' or not isinstance(result.text, str):
                        raise ValueError
                    self.response = result.text.strip()
                except (ET.ParseError, ValueError, IndexError):
                    self.violations.append("The response is not in the requested format.")
                    return False
            # case OutputType.WRAP:
            #     lines = response.split("\n")
            #     num_lines = self.wrap_lines
            #
            #     # if the response isn't long enough, only check the beginning and end
            #     if len(lines) < 2 * self.wrap_lines:
            #         num_lines = 1
            #     wrap_start = lines[:num_lines]
            #     wrap_end = lines[-num_lines:]
            #
            #     start_valid = False
            #     end_valid = False
            #     for line in wrap_start:
            #         start_valid |= line.startswith(self.wrap_text)
            #     for line in wrap_end:
            #         end_valid |= line.endswith(self.wrap_text)
            #
            #     # the response is only valid if it starts and ends with the correct text
            #     if not (start_valid & end_valid):
            #         self.violations.append("The response is not in the requested format.")
            #         return False
            #     else:
            #         parsed_start = [line.removeprefix(self.wrap_text) for line in wrap_start]
            #         parsed_end = [line.removesuffix(self.wrap_text) for line in wrap_end]
            #         self.response = '\n'.join(parsed_start + lines[num_lines:-num_lines] + parsed_end)

        return True

    def get_description(self) -> str:
        """
        Creates a description based on the output type. The description is used to generate prompts when
        executing DINOS/randomizer/run_randomizer.py.

        Returns:
            str: The description specific to the output type.
        """
        description = f"The response must be given in {self.output_type.name} format."
        match self.output_type:
            case OutputType.JSON | OutputType.YAML:
                description += " There should be a 'Response' key with corresponding value equal to the response."
            case OutputType.XML:
                description += " The root tag should be named 'Response' and should directly enclose the response."
            # case OutputType.WRAP:
            #     description = f"The response must be enclosed in '{self.wrap_text}' characters. That is, the response should start and end with '{self.wrap_text}'."

        return description
