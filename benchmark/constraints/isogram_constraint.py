import string

from benchmark.constraints.constraint import Constraint
from utils.problem_type import ProblemType

class IsogramConstraint(Constraint):
    problem_type = ProblemType.ELEMENT_CONSTRAINT
    """
    This constraint requires the models response to only use isograms. An
    isogram is a word that does not contain repeating letters.

    e.g.,
        you, are, a, genius  -->  isograms
        hello, goodbye --> not isograms
    """
    def __init__(self) -> None:
        super().__init__("Each word in the response must be an isogram.")

    def validate(self, response: str) -> bool:
        """
        Validates if the given response uses only isograms. Saves all non-isogram
        words to better measure performance.

        Arg:
            response (str): The response text to validate.

        Returns:
            bool: True if all words are isograms, False otherwise.
        """
        words = response.split()
        for word in words:

            # remove punctuation
            word_no_punc = word.strip(string.punctuation)

            seen = set()
            for letter in word_no_punc.lower():
                if letter in seen:
                    self.violations.append(word_no_punc)
                    break
                seen.add(letter)

        return False if len(self.violations) > 0 else True
