from abc import ABC, abstractmethod

class Constraint(ABC):
    def __init__(self, description: str = "") -> None:
        self.description = description

    @abstractmethod
    def validate(self, response: str) -> bool:
        pass
