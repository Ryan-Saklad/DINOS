from abc import ABC, abstractmethod

class Problem(ABC):
    def __init__(self) -> None:
        self.problem: str = ""
        self.answer: str = ""

    def generate(self) -> None:
        pass

    @abstractmethod
    def validate(self, response: str) -> bool:
        pass
