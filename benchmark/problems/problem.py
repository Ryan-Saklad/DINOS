import json
import random
import string

from abc import ABC, abstractmethod
from utils.problem_type import ProblemType

class BaseProblem(ABC):
    def __init__(self, seed: int | None = None) -> None:
        super().__init__()
        self.problem_types: list[ProblemType] = []
        self.seed: int | None = seed if seed is not None else random.randint(0, 1000000)
        self.rng: random.Random = random.Random(seed)

        self.answer: str = ""

        self.prompts = self.get_default_prompts()

    def get_default_prompts(self) -> dict:
        prompts = {}
        
        with open("benchmark/prompts/en/response_prompts.json", "r") as f:
            prompts.update(json.load(f))
        
        with open("benchmark/prompts/en/multiple_choice_prompts.json", "r") as f:
            prompts.update(json.load(f))
        
        with open(f"benchmark/prompts/en/{self.problem_name}_prompts.json", "r") as f:
            prompts.update(json.load(f))
        
        return prompts

    @abstractmethod
    def generate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def generate_prompt(self, num_shots: int = 0) -> None:
        """
        Generates a prompt for the problem.

        Args:
            num_shots (int): The number of example problems to include in the prompt. Default is 0.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_problem_str(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def generate_answer_str(self) -> None:
        raise NotImplementedError

    def validate(self, response: str) -> bool:
        return response == self.answer

    def get_answer(self) -> str:
        return self.answer

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
    def __init__(self, seed: int | None = None) -> None:
        super().__init__(seed)

        self.problem_types.append(ProblemType.RESPONSE)


class MultipleChoiceProblem(BaseProblem, ABC):
    def __init__(self, seed: int | None = None) -> None:
        super().__init__(seed)

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
        """
        Generates a list of option labels for multiple choice questions.

        Args:
            num_options (int): The number of option labels to generate.
            use_uppercase (bool): Whether to include uppercase letters. Default is True.
            use_lowercase (bool): Whether to include lowercase letters. Default is False.
            use_numbers (bool): Whether to include numbers. Default is False.
            prevent_same_letter_case (bool): Whether to prevent both lowercase and uppercase of the same letter from appearing. Default is False.
            randomize (bool): Whether to randomize the order of the option labels. Default is False.

        Returns:
            list[str]: A list of option labels.
        """
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
            self.rng.shuffle(options)

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

    def generate_multiple_choice_prompt(
        self, 
        multiple_choice_problem_prompt: str, 
        options: str, 
        multiple_choice_prompt: str | None = None,
        examples: str | None = None
    ) -> None:
        if multiple_choice_prompt is None:
            if examples:
                multiple_choice_prompt = self.prompts["multiple_choice_prompt_w_examples"]
            else:
                multiple_choice_prompt = self.prompts["multiple_choice_prompt"]

        self.prompt = multiple_choice_prompt.format(
            multiple_choice_problem_prompt=multiple_choice_problem_prompt,
            options=options,
            examples=examples if examples else ""
        )

    def generate_problem_json(self, problem_id: int | None = None) -> dict:
        problem_json = super().generate_problem_json(problem_id)
        problem_json.update({
            "options": self.options,
            "answer": self.answer
        })

        return problem_json
