import string
from benchmark.constraints.constraint import Constraint
from utils.problem_type import ProblemType

class PalindromeConstraint(Constraint):
    problem_type = ProblemType.ELEMENT_CONSTRAINT
    """Requires a model to respond to a prompt with a palindrome."""
    def __init__(self) -> None:
        super().__init__('The response should be a palindrome.')

    def validate(self, response: str, original_text: str = '') -> bool:
        """
        Validates the models response and saves the sequence if it is not a palindrome.

        Arg:
            response (str): The model's response.

        Returns:
            bool: True if the response is a palindrome, False otherwise.
        """
        fmt_response = self.strip_boilerplate(response)
        fmt_response = fmt_response.lower()
        fmt_response = ''.join(e for e in fmt_response if e.isalnum())
        return fmt_response == fmt_response[::-1]
