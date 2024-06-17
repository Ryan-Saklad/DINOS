from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class MathExpressionProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "math_expression_problem"
        super().__init__(**kwargs)

        self.operators: list[str] = ["+", "-", "*"]

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
        option_labels = self._generate_option_labels(
            num_options, 
            use_uppercase, 
            use_lowercase, 
            use_numbers, 
            prevent_same_letter_case, 
            randomize
        )

        option_pairs: list[tuple[str, ResponseProblem]]
        correct_label: str

        option_pairs, correct_label = self._create_additional_choices(option_labels, num_options)
        self.answer = correct_label
        self.options = dict(option_pairs)
        self.option_labels = option_labels

        if ProblemType.SOLVE_EXPRESSION not in self.problem_types and ProblemType.CHOOSE_MATCHING_EXPRESSION not in self.problem_types:
            if self.config.rng.choice([True, False]):
                self.problem_types.append(ProblemType.SOLVE_EXPRESSION)
            else:
                self.problem_types.append(ProblemType.CHOOSE_MATCHING_EXPRESSION)
        # Otherwise, one of the two problem types is already set

        self.prompt = self.render_template(examples=self._generate_examples(num_shots))

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
            new_problem = MathExpressionMultipleChoiceProblem(config=self.config)
            new_problem.problem_types = self.problem_types  # Guarentees the correct type of problem is created
            new_problem.generate(
                min_depth=self.min_depth, 
                max_depth=self.max_depth, 
                min_value=self.min_value, 
                max_value=self.max_value, 
                min_sub_expressions=self.min_sub_expressions, 
                max_sub_expressions=self.max_sub_expressions
            )

            if new_problem._answer != self._answer and new_problem.problem not in [option.problem for label, option in option_pairs if option is not None]:
                problems.append(new_problem)

        for i, (label, option) in enumerate(option_pairs):
            if option is None and problems:
                option_pairs[i] = (label, problems.pop(0))

        return option_pairs, correct_label
