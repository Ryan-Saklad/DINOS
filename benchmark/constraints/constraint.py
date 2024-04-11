from abc import ABC, abstractmethod
from utils.problem_type import ProblemType

class Constraint(ABC):
    def __init__(self, description: str = "") -> None:
        self.description = description
        self.violations: list[str] = []

        self.problem_type: ProblemType = ProblemType.CONSTRAINT

    @abstractmethod
    def validate(self, response: str) -> bool:
        pass
