import json
import random
import string

from abc import ABC, abstractmethod
from benchmark.config import Config
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

    def _generate_examples(self, num_shots: int, **kwargs) -> list['ResponseProblem']:
        examples = []
        for i in range(num_shots):
            self.config.increment_seed()
            # Create an instance of the subclass from which this method is called
            example_problem = type(self)(config=self.config, **kwargs)
            example_problem.generate()
            example_problem.generate_prompt(num_shots=0)
            examples.append(example_problem)
        return examples

    def generate_prompt(self, num_shots: int = 0) -> None:
        self.prompt: str = self.render_template(examples=self._generate_examples(num_shots))

class MultipleChoiceProblem(BaseProblem, ABC):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

        self.options: dict[str, str] = {}
        self.problem_types.append(ProblemType.MULTIPLE_CHOICE)

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

    @abstractmethod
    def generate_prompt(
        self, 
        num_shots: int = 0, 
        num_options: int = 2,
        use_uppercase: bool = True, 
        use_lowercase: bool = False, 
        use_numbers: bool = False, 
        prevent_same_letter_case: bool = False, 
        randomize: bool = False
    ) -> None:
        raise NotImplementedError

    def generate_problem_json(self, problem_id: int | None = None) -> dict:
        problem_json = super().generate_problem_json(problem_id)
        problem_json.update({
            "options": self.options,
            "answer": self.answer
        })

        return problem_json
