import random
from benchmark.problems.problem import Problem

class MathExpressionProblem(Problem):
    def __init__(self) -> None:
        super().__init__()
        self.prompt: str = "Please evaluate the following mathematical expression:"
        self.problem: str = ""
        self.answer: str = ""

    def generate(self, min_depth: int = 2, max_depth: int = 3, min_value: int = -9, max_value: int = 9, min_sub_expressions: int = 2, max_sub_expressions: int = 4) -> None:
        def generate_expression(depth: int, num_sub_expressions: int = 2) -> str:
            if depth == 1:
                return str(random.randint(min_value, max_value))
            else:
                sub_expressions = [generate_expression(depth - 1, generate_num_sub_expressions()) for _ in range(num_sub_expressions)]
                generated_operators = [random.choice(self.operators) for _ in range(num_sub_expressions - 1)]

                expression = sub_expressions[0]
                for i in range(num_sub_expressions - 1):
                    expression += f" {generated_operators[i]} {sub_expressions[i + 1]}"
                return f"({expression})"

        self.operators: list[str] = ["+", "-", "*"]
        depth: int = random.randint(min_depth, max_depth)
        num_sub_expressions: int = random.randint(min_sub_expressions, max_sub_expressions)
        generate_num_sub_expressions = lambda: random.randint(min_sub_expressions, max_sub_expressions)
        self.problem = generate_expression(depth, generate_num_sub_expressions())
        self.answer = str(eval(self.problem))

    def validate(self, response: str) -> bool:
        return self.answer == response
