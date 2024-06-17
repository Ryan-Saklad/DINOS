from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class DyckLanguageProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "dyck_language_problem"
        super().__init__(**kwargs)

        self.parens: list[tuple[str, str]] = [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]

        self.problems: dict[str, BaseProblem] = {
            "response": DyckLanguageResponseProblem,
            "multiple_choice": DyckLanguageMultipleChoiceProblem
        }

    def generate(self, min_length: int = 5, max_length: int = 10, **kwargs) -> None:
        self.min_length: int = min_length
        self.max_length: int = max_length
        self.length: int = self.config.rng.randint(min_length, max_length)

        def generate_dyck_word(length: int) -> str:
            if length == 0:
                return ""
            else:
                split = self.config.rng.randint(0, length - 1)
                left = generate_dyck_word(split)
                right = generate_dyck_word(length - split - 1)
                paren = self.config.rng.choice(self.parens)
                return f"{paren[0]}{left}{right}{paren[1]}"
        
        def valid_split_index(dyck_word: str) -> int:
            last_start_index = -1
            for i, char in enumerate(dyck_word):
                if char in "([{<":
                    last_start_index = i
            return last_start_index + 1 if last_start_index != -1 else len(dyck_word) // 2

        dyck_word = generate_dyck_word(self.length // 2 * 2)  # Ensure even length

        split_index = valid_split_index(dyck_word)
        random_split_index = self.config.rng.randint(split_index, len(dyck_word) - 1)

        self.problem = dyck_word[:random_split_index]
        self._answer = dyck_word[random_split_index:]
        self.answer: str = self._answer


class DyckLanguageResponseProblem(DyckLanguageProblem, ResponseProblem):
    pass


class DyckLanguageMultipleChoiceProblem(DyckLanguageProblem, MultipleChoiceProblem):
    def generate_prompt(self, **kwargs) -> None:
        if ProblemType.SOLVE_EXPRESSION not in self.problem_types:
            self.problem_types.append(ProblemType.SOLVE_EXPRESSION)
        super().generate_prompt(**kwargs)
