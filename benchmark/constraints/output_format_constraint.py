from benchmark.constraints.constraint import Constraint
from utils.output_type import OutputType


class OutputFormatConstraint(Constraint):
    def __init__(self, output_type: OutputType):
        """
        Initializes the output format type constraint.

        Args:
            output_type (OutputType): Specifies the output format expected in validation (e.g., json, yaml)

        Raises:
            ValueError: If the provided output type is not of OutputType.
        """
        if not isinstance(output_type, OutputType):
            raise ValueError("output_type must be an instance of OutputType")

        self.output_type: OutputType = output_type

        super().__init__(f"{output_type.name.lower()} output format constraint.")

    def validate(self, response: str) -> bool:
        """
        Validates if the given string is given in the expected output format.

        Args:
            response (str): The response text to validate.

        Returns:
            bool: True if the response matches the expected output format, False otherwise.
        """
        pass

