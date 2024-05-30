from enum import Enum, auto

class ProblemType(Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    RESPONSE = "RESPONSE"

    def __str__(self):
        return self.value
