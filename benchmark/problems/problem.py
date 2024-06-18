import json
import random
import string

from abc import ABC, abstractmethod
from benchmark.config import Config
from enum import Enum
from utils.problem_type import ProblemType


class BaseProblem(ABC):
    def __init__(self, config: Config) -> None:
        super().__init__()

        self.config: Config = config
        self.config.increment_seed()  # Allows for example creation to work properly
        self.problem_types: list[ProblemType] = []
        self.seed: int = config.seed

    def render_template(self, examples: list["BaseProblem"] | None = None, **kwargs) -> str:
        return self.config.render_template(self, examples, **kwargs)

    @abstractmethod
    def generate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def generate_prompt(self, num_shots: int = 0) -> None:
        raise NotImplementedError

    def _generate_examples(self, num_shots: int) -> list["BaseProblem"]:
        examples = []
        for i in range(num_shots):
            self.config.increment_seed()
            # Create an instance of the subclass from which this method is called
            example_problem = type(self)(config=self.config)
            example_problem.problem_types = self.problem_types  # Guarentees the correct type of problem is created
            example_problem.generate(**vars(self))
            example_problem.generate_prompt(num_shots=0)
            examples.append(example_problem)

        return examples

    def generate_problem_json(self, problem_id: int | None = None) -> dict:
        if problem_id is None:
            return {
                f"{self.problem_name}_{'_'.join([str(pt) for pt in self.problem_types])}_{self.seed}": {
                    "problem_name": self.problem_name,
                    "prompt": self.prompt,
                    "answer": self.answer,
                    "problem_types": [str(pt) for pt in self.problem_types]
                }
            }
        else:
            return {
                f"{problem_id}": {
                    "problem_name": self.problem_name,
                    "prompt": self.prompt,
                    "answer": self.answer,
                    "problem_types": [str(pt) for pt in self.problem_types]
                }
            }


class ResponseProblem(BaseProblem, ABC):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.problem_types.append(ProblemType.RESPONSE)

    def generate_prompt(self, num_shots: int = 0) -> None:
        self.prompt: str = self.render_template(examples=self._generate_examples(num_shots))


class AlternativeAnswer(Enum):
    NONE_OF_THE_ABOVE = "None of the above"
    NONE_OF_THE_BELOW = "None of the below"
    NONE_OF_THE_OTHER_ANSWERS = "None of the other answers"


class MultipleChoiceProblem(BaseProblem, ABC):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.options: dict[str, str] = {}
        self.problem_types.append(ProblemType.MULTIPLE_CHOICE)
        self.alternate_display_answers: dict[str, AlternativeAnswer] = {}

    def generate_prompt(
        self,
        problem_types: list[ProblemType] | ProblemType,
        num_shots: int = 0,
        num_options: int = 4,
        use_uppercase: bool = True,
        use_lowercase: bool = False,
        use_numbers: bool = False,
        prevent_same_letter_case: bool = False,
        randomize: bool = False,
        no_other_answer_probability: float = 0.25
    ) -> None:
        if not 0.0 <= no_other_answer_probability <= 1.0:
            raise ValueError("no_other_answer_probability must be between 0 and 1")

        if isinstance(problem_types, ProblemType):
            problem_types = [problem_types]

        for problem_type in problem_types:
            if problem_type not in self.problem_types:
                self.problem_types.append(problem_type)

        option_labels = self._generate_option_labels(
            num_options, 
            use_uppercase, 
            use_lowercase, 
            use_numbers, 
            prevent_same_letter_case, 
            randomize
        )

        if num_options > len(option_labels):
            raise ValueError("Number of options requested exceeds the available unique labels.")

        option_pairs: list[tuple[str, ResponseProblem]]
        correct_label: str

        option_pairs, correct_label = self._create_additional_choices(option_labels, num_options)

        if self.config.rng.random() < no_other_answer_probability:
            choice = self.config.rng.choice([1, 2, 3])
            if choice == 1:
                random_index = self.config.rng.randint(0, len(option_pairs) - 1)
                self.alternate_display_answers[option_pairs[random_index][0]] = AlternativeAnswer.NONE_OF_THE_OTHER_ANSWERS
            elif choice == 2:
                self.alternate_display_answers[option_pairs[-1][0]] = AlternativeAnswer.NONE_OF_THE_ABOVE
            elif choice == 3:
                self.alternate_display_answers[option_pairs[0][0]] = AlternativeAnswer.NONE_OF_THE_BELOW

        self.answer = correct_label
        self.options = dict(option_pairs)
        self.option_labels = option_labels

        self.prompt = self.render_template(examples=self._generate_examples(num_shots))

    def _generate_option_labels(
        self, 
        num_options: int, 
        use_uppercase: bool = True, 
        use_lowercase: bool = False, 
        use_numbers: bool = False, 
        prevent_same_letter_case: bool = False, 
        randomize: bool = False
    ) -> list[str]:
        options = []
        if use_uppercase:
            options.extend(string.ascii_uppercase)
        if use_lowercase:
            options.extend(string.ascii_lowercase)
        if use_numbers:
            options.extend(string.digits)

        if prevent_same_letter_case:
            filtered_options = []
            seen_letters = set()
            for option in options:
                letter = option.lower()
                if letter not in seen_letters:
                    filtered_options.append(option)
                    seen_letters.add(letter)
            options = filtered_options

        if num_options > len(options):
            raise ValueError("Number of options requested exceeds the available unique labels.")

        if randomize:
            self.config.rng.shuffle(options)

        return options[:num_options]

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
            new_problem = self.problems["response"](config=self.config)
            new_problem.problem_types = self.problem_types  # Guarentees the correct type of problem is created
            new_problem.generate(**vars(self))

            if new_problem._answer != self._answer and new_problem.problem not in [option.problem for label, option in option_pairs if option is not None]:
                problems.append(new_problem)

        for i, (label, option) in enumerate(option_pairs):
            if option is None and problems:
                option_pairs[i] = (label, problems.pop(0))

        return option_pairs, correct_label

    def generate_problem_json(self, problem_id: int | None = None) -> dict:
        problem_json = super().generate_problem_json(problem_id)
        problem_json.update({
            "options": self.options,
            "answer": self.answer
        })

        return problem_json
