import random

from benchmark.problems.problem import Problem

class BooleanExpressionProblem(Problem):
    def __init__(self) -> None:
        super().__init__()
        self.prompt: str = "Please evaluate the following boolean expression with 'True' or 'False' as the answer:"
        self.problem: str = ""
        self.answer: str = ""

    def generate(self, min_depth: int = 3, max_depth: int = 5) -> None:
        def generate_expression(depth: int) -> str:
            if depth == 1:
                return random.choice(self.bool_values)
            else:
                sub_expr1 = generate_expression(depth - 1)
                sub_expr2 = generate_expression(depth - 1)

                # Randomly choose to use a unary operator or a binary operator
                if random.random() < 0.5:
                    return f"{self.unary_operator} ({sub_expr1})"
                else:
                    operator = random.choice(self.operators)
                    return f"({sub_expr1}) {operator} ({sub_expr2})"

        self.bool_values: list[str] = ["True", "False"]
        self.operators: list[str] = ["and", "or"]
        self.unary_operator: str = "not"

        depth: int = random.randint(min_depth, max_depth)

        self.problem = generate_expression(depth)
        self.problem = self.problem.replace("(True)", "True").replace("(False)", "False")
        self.problem = self.problem.replace("(not True)", "not True").replace("(not False)", "not False")

        self.answer = self.evaluate(self.problem)

    def evaluate(self, expression: str) -> str:
        return str(eval(expression))

    def validate(self, response: str) -> bool:
        return self.answer == response
