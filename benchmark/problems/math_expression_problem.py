from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class MathExpressionProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "math_expression_problem"
        super().__init__(**kwargs)

        self.operators: list[str] = ["+", "-", "*"]

        self.problems: dict[str, BaseProblem] = {
            "response": MathExpressionResponseProblem,
            "multiple_choice": MathExpressionMultipleChoiceProblem
        }

    def generate(self, min_depth: int = 2, max_depth: int = 3, min_value: int = -9, max_value: int = 9, min_sub_expressions: int = 2, max_sub_expressions: int = 4, **kwargs) -> None:
        def generate_expression(depth: int, num_sub_expressions: int = 2) -> str:
            if depth == 1:
                return str(self.config.rng.randint(min_value, max_value))
            else:
                sub_expressions = [generate_expression(depth - 1, self.config.rng.randint(min_sub_expressions, max_sub_expressions)) for _ in range(num_sub_expressions)]
                generated_operators = [self.config.rng.choice(self.operators) for _ in range(num_sub_expressions - 1)]
                
                expression = sub_expressions[0]
                for i in range(num_sub_expressions - 1):
                    expression += f" {generated_operators[i]} {sub_expressions[i + 1]}"
                
                return f"({expression})"

        self.min_depth: int = min_depth
        self.max_depth: int = max_depth
        self.min_value: int = min_value
        self.max_value: int = max_value
        self.min_sub_expressions: int = min_sub_expressions
        self.max_sub_expressions: int = max_sub_expressions
        
        depth: int = self.config.rng.randint(min_depth, max_depth)
        num_sub_expressions: int = self.config.rng.randint(min_sub_expressions, max_sub_expressions)
        
        self.problem = generate_expression(depth, num_sub_expressions)
        self._answer = str(eval(self.problem))
        self.answer: str = self._answer


class MathExpressionResponseProblem(MathExpressionProblem, ResponseProblem):
    pass


class MathExpressionMultipleChoiceProblem(MathExpressionProblem, MultipleChoiceProblem):
    def generate_prompt(self, **kwargs) -> None:
        if ProblemType.SOLVE_EXPRESSION not in self.problem_types and ProblemType.CHOOSE_MATCHING_EXPRESSION not in self.problem_types:
            if self.config.rng.choice([True, False]):
                super().generate_prompt(ProblemType.SOLVE_EXPRESSION, **kwargs)
            else:
                super().generate_prompt(ProblemType.CHOOSE_MATCHING_EXPRESSION, **kwargs)
        elif ProblemType.SOLVE_EXPRESSION in self.problem_types:
            super().generate_prompt(ProblemType.SOLVE_EXPRESSION, **kwargs)
        elif ProblemType.CHOOSE_MATCHING_EXPRESSION in self.problem_types:
            super().generate_prompt(ProblemType.CHOOSE_MATCHING_EXPRESSION, **kwargs)
        else:
            raise ValueError("Invalid problem type")
