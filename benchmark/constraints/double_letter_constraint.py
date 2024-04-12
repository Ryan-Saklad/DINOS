import string
from benchmark.constraints.constraint import Constraint


class DoubleLetterConstraint(Constraint):
    """Requires a model to respond to a prompt without using words that contain
    double letters."""
    def __init__(self) -> None:
        super().__init__('No words in the response should contain double letters. '
                         'That is, for a given word in the response, no consecutive '
                         'letters should be the same.')

    def validate(self, response: str) -> bool:
        """
        Validates the models response and saves words that contain double letters,
        if any. A double letter word is not the same as an isogram. A double letter
        word contains at least one letter that appears consecutively.

        Arg:
            response (str): The model's response.

        Returns:
            bool: True if no words with double letters are found, False otherwise.
        """
        words = response.split()
        for word in words:

            # remove punctuation
            word_no_punc = word.strip(string.punctuation)

            if len(word_no_punc) == 1:
                continue

            for i in range(len(word_no_punc) - 1):
                if word_no_punc[i].lower() == word_no_punc[i + 1].lower():
                    self.violations.append(word_no_punc)
                    break

        return False if len(self.violations) > 0 else True
