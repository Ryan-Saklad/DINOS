import json

from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class LiarProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "liar_problem"
        super().__init__(**kwargs)

        with open("utils/names.json") as f:
            self.names: list[str] = json.load(f)["names"]

        self.truthfulness: dict[str, bool] = {}
        self.statements: list[str] = []
        self.final_truth: bool = False
        self.statement_style: bool = False

        self.problems: dict[str, BaseProblem] = {
            "response": LiarResponseProblem,
            "multiple_choice": LiarMultipleChoiceProblem
        }
        
    def generate(self, num_people: int = 5, **kwargs) -> None:
        self.num_people = num_people
        self.names = self.config.rng.sample(self.names, num_people)
        self.truthfulness = {name: self.config.rng.choice([True, False]) for name in self.names}
        self.statement_style = self.config.rng.choice([True, False])
        
        if self.truthfulness[self.names[0]]:
            self.statements.append(f"{self.names[0]} always tells the truth.")
        else:
            self.statements.append(f"{self.names[0]} always lies.")
        
        for i in range(1, num_people):
            previous_name = self.names[i - 1]
            current_name = self.names[i]
            
            if self.statement_style:  # Current about Previous
                if self.truthfulness[current_name]:
                    if self.truthfulness[previous_name]:
                        self.statements.append(f"{current_name} says {previous_name} tells the truth.") 
                    else:
                        self.statements.append(f"{current_name} says {previous_name} lies.")
                else:
                    if self.truthfulness[previous_name]:
                        self.statements.append(f"{current_name} says {previous_name} lies.")
                    else:
                        self.statements.append(f"{current_name} says {previous_name} tells the truth.")
            else:  # Previous about Current
                if self.truthfulness[previous_name]:
                    if self.truthfulness[current_name]:
                        self.statements.append(f"{previous_name} says {current_name} tells the truth.")
                    else:
                        self.statements.append(f"{previous_name} says {current_name} lies.")
                else:
                    if self.truthfulness[current_name]:
                        self.statements.append(f"{previous_name} says {current_name} tells the truth.")
                    else:
                        self.statements.append(f"{previous_name} says {current_name} lies.")

        self.problem: str = " ".join(self.statements)
        self._answer = str(self.truthfulness[self.names[-1]])
        self.answer: str = self._answer


class LiarResponseProblem(LiarProblem, ResponseProblem):
    pass


class LiarMultipleChoiceProblem(LiarProblem, MultipleChoiceProblem):
    def generate_prompt(self, **kwargs) -> None:
        if ProblemType.CHOOSE_MATCHING_EXPRESSION not in self.problem_types:
            self.problem_types.append(ProblemType.CHOOSE_MATCHING_EXPRESSION)
        super().generate_prompt(**kwargs)
