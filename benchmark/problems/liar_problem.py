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

    def _create_additional_choices(self, option_labels: list[str], num_options: int) -> tuple[list[tuple[str, ResponseProblem]], str, int]:
        option_pairs: list[tuple[str, ResponseProblem]] = [(label, None) for label in option_labels]

        # Set the correct answer to this problem to a random label
        random_label = self.config.rng.choice([label for label, option in option_pairs if option is None])
        for i, (label, option) in enumerate(option_pairs):
            if label == random_label:
                option_pairs[i] = (label, self)
                correct_label = label
                break

        problems = []
        while len(problems) < num_options - 1:
            self.config.increment_seed()
            new_problem = LiarResponseProblem(config=self.config)
            new_problem.generate(num_people=self.num_people)

            if new_problem._answer != self._answer and new_problem.problem not in [option.problem for label, option in option_pairs if option is not None]:
                problems.append(new_problem)

        for i, (label, option) in enumerate(option_pairs):
            if option is None and problems:
                option_pairs[i] = (label, problems.pop(0))

        return option_pairs, correct_label
