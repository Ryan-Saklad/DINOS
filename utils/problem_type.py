from enum import Enum, auto

class ProblemType(Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    RESPONSE = "RESPONSE"

    # E.g. Select the choice that correctly evaluates ?.
    SOLVE_EXPRESSION = "SOLVE_EXPRESSION"

    # E.g. Select the choice that evaluates to ?.
    CHOOSE_MATCHING_EXPRESSION = "CHOOSE_MATCHING_EXPRESSION"

    def __str__(self):
        return self.value
