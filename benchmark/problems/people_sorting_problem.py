import json

from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class PeopleSortingProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "people_sorting_problem"
        super().__init__(**kwargs)

        with open("utils/names.json") as f:
            self.names: list[str] = json.load(f)["names"]

        self.problems: dict[str, BaseProblem] = {
            "response": PeopleSortingResponseProblem,
            "multiple_choice": PeopleSortingMultipleChoiceProblem
        }

    def generate(self, num_names: int = 15, **kwargs) -> None:
        self.num_names = num_names
        self.names_sample = self.config.rng.sample(self.names, num_names)

        self.problem = " ".join(self.names_sample)
        self._answer = " ".join(sorted(self.names_sample))
        self.answer = self._answer


class PeopleSortingResponseProblem(PeopleSortingProblem, ResponseProblem):
    pass


class PeopleSortingMultipleChoiceProblem(PeopleSortingProblem, MultipleChoiceProblem):
    def generate_prompt(self, **kwargs) -> None:
        super().generate_prompt(ProblemType.SOLVE_EXPRESSION, **kwargs)

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
        sorted_names = sorted(self.names_sample)
        while len(problems) < num_options - 1:
            self.config.increment_seed()
            new_problem = self.__class__(**self.__dict__)

            # Generate a unique permutation by swapping two neighboring names
            for i in range(len(sorted_names) - 1):
                permuted_names = sorted_names[:]
                permuted_names[i], permuted_names[i + 1] = permuted_names[i + 1], permuted_names[i]
                new_problem._answer = " ".join(permuted_names)

                if all(new_problem._answer != problem._answer for problem in problems):
                    problems.append(new_problem)
                    break

        for i, (label, option) in enumerate(option_pairs):
            if option is None and problems:
                option_pairs[i] = (label, problems.pop(0))

        return option_pairs, correct_label
