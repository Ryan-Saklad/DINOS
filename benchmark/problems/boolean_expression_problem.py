from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class BooleanExpressionProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "boolean_expression_problem"
        super().__init__(**kwargs)

        self.bool_values: list[str] = ["True", "False"]
        self.operators: list[str] = ["and", "or"]
        self.unary_operator: str = "not"

    def generate(self, min_depth: int = 3, max_depth: int = 4, **kwargs) -> None:
        if not isinstance(min_depth, int) or not isinstance(max_depth, int):
            raise ValueError("min_depth and max_depth must be integers")
        if min_depth < 1 or max_depth < min_depth:
            raise ValueError("min_depth must be >= 1 and max_depth must be >= min_depth")

        self.min_depth: int = min_depth
        self.max_depth: int = max_depth
        self.depth: int = self.config.rng.randint(min_depth, max_depth)

        def generate_expression(depth: int) -> str:
            if depth == 1:
                return self.config.rng.choice(self.bool_values)
            else:
                sub_expr1 = generate_expression(depth - 1)
                sub_expr2 = generate_expression(depth - 1)

                # Randomly choose to use a unary operator or a binary operator
                if self.config.rng.random() < 0.5:
                    return f"{self.unary_operator} ({sub_expr1})"
                else:
                    operator = self.config.rng.choice(self.operators)
                    return f"({sub_expr1}) {operator} ({sub_expr2})"

        self.problem: str = generate_expression(self.depth)
        self._answer: str = self._evaluate(self.problem)
        self.answer: str = self._answer

    def _evaluate(self, expression: str) -> str:
        return str(eval(expression))


class BooleanExpressionResponseProblem(BooleanExpressionProblem, ResponseProblem):
    pass


class BooleanExpressionMultipleChoiceProblem(BooleanExpressionProblem, MultipleChoiceProblem):
    def generate_prompt(self, **kwargs) -> None:
        if ProblemType.CHOOSE_MATCHING_EXPRESSION not in self.problem_types:
            self.problem_types.append(ProblemType.CHOOSE_MATCHING_EXPRESSION)
        super().generate_prompt(**kwargs)

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
            new_problem = BooleanExpressionResponseProblem(config=self.config)
            new_problem.generate(min_depth=self.depth, max_depth=self.depth)

            if new_problem._answer != self._answer and new_problem.problem not in [option.problem for label, option in option_pairs if option is not None]:
                problems.append(new_problem)

        for i, (label, option) in enumerate(option_pairs):
            if option is None and problems:
                option_pairs[i] = (label, problems.pop(0))

        return option_pairs, correct_label
