import random
from benchmark.problems.problem import Problem

class MathExpressionProblem(Problem):
    def __init__(self) -> None:
        super().__init__()
        self.prompt: str = "Please evaluate the following mathematical expression:"
        self.problem: str = ""
        self.answer: str = ""

    def generate(self, min_depth: int = 2, max_depth: int = 4, min_value: int = -10, max_value: int = 10) -> None:
        def generate_expression(depth: int) -> str:
            if depth == 1:
                return str(random.randint(min_value, max_value))
            else:
                sub_expr1 = generate_expression(depth - 1)
                sub_expr2 = generate_expression(depth - 1)
                operator = random.choice(self.operators)
                return f"({sub_expr1} {operator} {sub_expr2})"

        self.operators: list[str] = ["+", "-", "*"]
        depth: int = random.randint(min_depth, max_depth)
        self.problem = generate_expression(depth)
        self.answer = str(eval(self.problem))

    def validate(self, response: str) -> bool:
        return self.answer == response
