from enum import Enum, auto

class ProblemType(Enum):
    ELEMENT_CONSTRAINT = "ELEMENT_CONSTRAINT"
    OUTPUT_FORMAT = "OUTPUT_FORMAT"
    PROBLEM = "PROBLEM"
    def __str__(self):
        return self.value
