import random

from benchmark.problems.problem import Problem
from utils.names import names

class LiarProblem(Problem):
    def __init__(self) -> None:
        super().__init__()
        self.prompt: str = "Determine the truthfulness ('True' or 'False') of the last person based on the following statements:"
        self.names: list[str] = names
        self.truthfulness: dict[str, bool] = {}
        self.statements: list[str] = []
        self.final_truth: bool = False
        self.statement_style: bool = random.choice([True, False])

    def generate(self, num_people: int = 5) -> None:
        self.names = random.sample(CHARACTER_NAMES, num_people)
        self.truthfulness = {name: random.choice([True, False]) for name in self.names}

        self.statements.append(f"{self.names[0]} always {'tells the truth' if self.truthfulness[self.names[0]] else 'lies'}.")

        for i in range(1, num_people):
            previous_name = self.names[i - 1]
            current_name = self.names[i]
            if self.statement_style:  # Current about Previous
                if self.truthfulness[current_name]:
                    self.statements.append(f"{current_name} says {previous_name} {'tells the truth' if self.truthfulness[previous_name] else 'lies'}.")
                else:
                    self.statements.append(f"{current_name} says {previous_name} {'tells the truth' if not self.truthfulness[previous_name] else 'lies'}.")
            else:  # Previous about Current
                if self.truthfulness[previous_name]:
                    self.statements.append(f"{previous_name} says {current_name} {'tells the truth' if self.truthfulness[current_name] else 'lies'}.")
                else:
                    self.statements.append(f"{previous_name} says {current_name} {'tells the truth' if not self.truthfulness[current_name] else 'lies'}.")

        self.statements.append(f"Is {self.names[-1]} telling the truth? Answer 'True' or 'False'.")

        self.problem = " ".join(self.statements)
        self.answer = str(self.truthfulness[self.names[-1]])

    def validate(self, response: str) -> bool:
        return str(self.truthfulness[self.names[-1]]) == response
