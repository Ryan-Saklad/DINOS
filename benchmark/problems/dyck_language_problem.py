from benchmark.problems.problem import Problem
from utils.problem_type import ProblemType

class DyckLanguageProblem(Problem):
    problem_type = ProblemType.PROBLEM
    def __init__(self) -> None:
        super().__init__()
        self.prompt: str = "Complete the following sequence, ensuring the parentheses are properly closed:"
        self.problem: str = ""
        self.answer: str = ""

    def generate(self, min_length: int = 5, max_length: int = 10) -> None:
        def generate_dyck_word(length: int) -> str:
            if length == 0:
                return ""
            elif length == 1:
                return self.rng.choice(self.parens)
            else:
                split = self.rng.randint(0, length - 1)
                left = generate_dyck_word(split)
                right = generate_dyck_word(length - split - 1)
                paren = self.rng.choice(self.parens)
                return f"{paren[0]}{left}{right}{paren[1]}"

        self.parens: list[tuple[str, str]] = [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]
        length: int = self.rng.randint(min_length, max_length)
        self.problem = generate_dyck_word(length // 2)  # Dyck words have even length

        # Ensure there are no starting parentheses left
        last_start_char_index = max(self.problem.rfind(paren[0]) for paren in self.parens)
        split_index = self.rng.randint(last_start_char_index + 1, len(self.problem) - 1)
        self.answer = self.problem[split_index:]
        self.problem = self.problem[:split_index]

    def validate(self, response: str) -> bool:
        return self.answer == response
