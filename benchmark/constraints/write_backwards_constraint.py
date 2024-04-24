from benchmark.constraints.constraint import Constraint
from utils.problem_type import ProblemType

class WriteBackwardsConstraint(Constraint):
    problem_type = ProblemType.ELEMENT_CONSTRAINT
    """Requires a model to respond to a prompt with the text written backwards."""
    def __init__(self) -> None:
        super().__init__('The response should be the text written backwards.')

    def validate(self, response: str, original_text: str = '') -> bool:
        """
        Validates if the model's response is the original text written backwards.

        Args:
            response (str): The model's response.
            original_text (str): The original text provided to the model.

        Returns:
            bool: True if the response is the original text written backwards, False otherwise.
        """
        fmt_response = self.strip_boilerplate(response)
        expected_response = original_text[::-1]
        return fmt_response == expected_response
