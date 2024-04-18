import string
from benchmark.constraints.constraint import Constraint

class PalindromeConstraint(Constraint):
    """Requires a model to respond to a prompt with a palindrome."""
    def __init__(self) -> None:
        super().__init__('The response should be a palindrome.')

    def validate(self, response: str) -> bool:
        """
        Validates the models response and saves the sequence if it is not a palindrome.

        Arg:
            response (str): The model's response.

        Returns:
            bool: True if the response is a palindrome, False otherwise.
        """
        response = response.lower()
        response = ''.join(e for e in response if e.isalnum())
        return response == response[::-1]
