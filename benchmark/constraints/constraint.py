from abc import ABC, abstractmethod
from utils.problem_type import ProblemType

class Constraint(ABC):
    def __init__(self, description: str = "") -> None:
        self.description = description
        self.violations: list[str] = []
        self.category = ""

        self.problem_type: ProblemType = ProblemType.ELEMENT_CONSTRAINT

    @abstractmethod
    def validate(self, response: str, original_text: str = '') -> bool:
        pass

    def get_description(self) -> str:
        return self.description

    def get_violations(self) -> list[str]:
        return self.violations
