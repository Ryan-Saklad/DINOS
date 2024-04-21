import random

from abc import ABC, abstractmethod
from utils.problem_type import ProblemType

class Problem(ABC):
    def __init__(self, seed: int | None = None) -> None:
        self.problem: str = ""
        self.answer: str = ""
        self.rng: random.Random = random.Random(seed if seed is not None else random.randint(0, 1000000))
        self.problem_type: ProblemType = ProblemType.PROBLEM

    def generate(self) -> None:
        pass

    @abstractmethod
    def validate(self, response: str) -> bool:
        pass

    def get_description(self, include_problem: bool = True) -> str:
        if include_problem:
            return f"{self.prompt}\n{self.problem}"
        else:
            return self.prompt

    def get_answer(self) -> str:
        return self.answer