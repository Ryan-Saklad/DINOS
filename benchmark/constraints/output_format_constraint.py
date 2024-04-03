import json
import yaml
import xml.etree.ElementTree as ET

from benchmark.constraints.constraint import Constraint
from utils.output_type import OutputType


class OutputFormatConstraint(Constraint):
    def __init__(self, output_type: OutputType, wrap_text: str = "", wrap_lines: int = 3):
        """
        Initializes the output format type constraint.

        Args:
            output_type (OutputType): Specifies the output format expected in validation (e.g., json, yaml).
            wrap_text (str): The text to wrap output in (e.g., ###, $$$).
            wrap_lines (int): The number of lines to check for wrapping text. Defaults to 3 to ignore boilerplate
                responses and system tokens. A higher value will trade off false negatives for false positives.

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

        super().__init__(f"{output_type.name.lower()} output format constraint.")

    def validate(self, response: str) -> bool:
        """
        Validates if the given string is given in the expected output format.

        Args:
            response (str): The response text to validate.

        Returns:
            bool: True if the response matches the expected output format, False otherwise.
        """
        match self.output_type:
            case OutputType.JSON:
                try:
                    json.loads(response)
                except json.decoder.JSONDecodeError:
                    self.violations.append("The response is not in json format.")
                    return False
            case OutputType.YAML:
                try:
                    yaml.safe_load(response)
                except yaml.YAMLError:
                    self.violations.append("The response is not in yaml format.")
                    return False
            case OutputType.XML:
                try:
                    ET.fromstring(response)
                except ET.ParseError:
                    self.violations.append("The response is not in xml format.")
                    return False
            case OutputType.WRAP:
                lines = response.split("\n")
                num_lines = self.wrap_lines

                # if the response isn't long enough, only check the beginning and end
                if len(lines) < 2 * self.wrap_lines:
                    num_lines = 1
                wrap_start = lines[:num_lines]
                wrap_end = lines[-num_lines:]

                start_valid = False
                end_valid = False
                for line in wrap_start:
                    start_valid |= line.startswith(self.wrap_text)
                for line in wrap_end:
                    end_valid |= line.endswith(self.wrap_text)

                # the response is only valid if it starts and ends with the correct text
                if not (start_valid & end_valid):
                    self.violations.append("The response is not in wrap format.")
                    return False

        return True
