from enum import Enum

from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem

class MathExpressionProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "math_expression_problem"
        super().__init__(**kwargs)

        self.operators: list[str] = ["+", "-", "*"]

    def generate(self, min_depth: int = 2, max_depth: int = 3, min_value: int = -9, max_value: int = 9, min_sub_expressions: int = 2, max_sub_expressions: int = 4) -> None:
        def generate_expression(depth: int, num_sub_expressions: int = 2) -> str:
            if depth == 1:
                return str(self.rng.randint(min_value, max_value))
            else:
                sub_expressions = [generate_expression(depth - 1, self.rng.randint(min_sub_expressions, max_sub_expressions)) for _ in range(num_sub_expressions)]
                generated_operators = [self.rng.choice(self.operators) for _ in range(num_sub_expressions - 1)]
                
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
        
        depth: int = self.rng.randint(min_depth, max_depth)
        num_sub_expressions: int = self.rng.randint(min_sub_expressions, max_sub_expressions)
        
        self._problem = generate_expression(depth, num_sub_expressions)
        self.problem = self._problem
        self._answer = str(eval(self.problem))
        self.answer = self._answer


class MathExpressionResponseProblem(MathExpressionProblem, ResponseProblem):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def generate_prompt(self, num_shots: int = 0) -> None:
        examples_str = self._generate_examples(num_shots)
        
        if examples_str:
            self.prompt = self.prompts["response_prompt_w_examples"].format(
                response_problem_prompt=self.prompts["response_problem_prompt"],
                response_problem=self.problem,
                examples=examples_str
            )
        else:
            self.prompt = self.prompts["response_prompt"].format(
                response_problem_prompt=self.prompts["response_problem_prompt"],
                response_problem=self.problem
            )

    def _generate_examples(self, num_shots: int) -> str:
        examples = []
        for i in range(num_shots):
            example_problem = MathExpressionResponseProblem(seed=self.seed + i)
            example_problem.generate(
                min_depth=self.min_depth,
                max_depth=self.max_depth,
                min_value=self.min_value,
                max_value=self.max_value,
                min_sub_expressions=self.min_sub_expressions,
                max_sub_expressions=self.max_sub_expressions
            )
            example_problem.generate_prompt(num_shots=0)
            examples.append(self.prompts["response_example"].format(problem_prompt=example_problem.prompt, answer=example_problem.answer))
        
        return "".join(example for example in examples)


class MathExpressionType(Enum):
    MC_EVALUATE_PROBLEM = 1
    MC_SELECT_PROBLEM = 2


class MathExpressionMultipleChoiceProblem(MathExpressionProblem, MultipleChoiceProblem):
    def generate_prompt(
        self,
        num_shots: int = 0, 
        num_options: int = 2,
        use_uppercase: bool = True, 
        use_lowercase: bool = False, 
        use_numbers: bool = False, 
        prevent_same_letter_case: bool = False, 
        randomize: bool = False,
        include_evaluate_expression: bool = True, 
        include_select_expression: bool = True
    ) -> None:
        if include_evaluate_expression and include_select_expression:
            if self.rng.choice([True, False]):
                self.generate_prompt_evaluate_expression(num_shots, num_options, use_uppercase, use_lowercase, use_numbers, prevent_same_letter_case, randomize)
            else:
                self.generate_prompt_select_expression(num_shots, num_options, use_uppercase, use_lowercase, use_numbers, prevent_same_letter_case, randomize)
        elif include_evaluate_expression:
            self.generate_prompt_evaluate_expression(num_shots, num_options, use_uppercase, use_lowercase, use_numbers, prevent_same_letter_case, randomize)
        elif include_select_expression:
            self.generate_prompt_select_expression(num_shots, num_options, use_uppercase, use_lowercase, use_numbers, prevent_same_letter_case, randomize)
        else:
            raise ValueError("At least one of include_evaluate_expression or include_select_expression must be True")

    def generate_prompt_evaluate_expression(
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

        values, seed_increment = self._create_additional_choices(num_options, MathExpressionType.MC_EVALUATE_PROBLEM)
        self.options = dict(zip(option_labels, values))
        self.option_labels = option_labels

        options_str = "\n".join(
            [self.prompts["multiple_choice_answer_choice"].format(label=label, option=option) 
             for label, option in zip(option_labels, values)]
        )
        correct_label = next(label for label, option in self.options.items() if option == self.answer)
        self.answer = correct_label

        examples_str = self._generate_examples_for_multiple_choice(
            num_shots,
            num_options,
            use_uppercase,
            use_lowercase,
            use_numbers,
            prevent_same_letter_case,
            randomize,
            seed_increment,
            include_evaluate_expression=True,
            include_select_expression=False
        )

        self.generate_multiple_choice_prompt(
            self.prompts["multiple_choice_evaluate_problem_prompt"].format(problem=self.problem),
            options_str,
            examples=examples_str if examples_str else None
        )

    def generate_prompt_select_expression(
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

        values, seed_increment = self._create_additional_choices(num_options, MathExpressionType.MC_SELECT_PROBLEM)
        self.options = dict(zip(option_labels, values))
        self.option_labels = option_labels

        options_str = "\n".join(
            [self.prompts["multiple_choice_answer_choice"].format(label=label, option=option) 
             for label, option in zip(option_labels, values)]
        )
        correct_label = next(label for label, option in self.options.items() if option == self.problem)
        self.answer = correct_label

        examples_str = self._generate_examples_for_multiple_choice(
            num_shots,
            num_options,
            use_uppercase,
            use_lowercase,
            use_numbers,
            prevent_same_letter_case,
            randomize,
            seed_increment,
            include_evaluate_expression=False,
            include_select_expression=True
        )

        self.generate_multiple_choice_prompt(
            self.prompts["multiple_choice_select_problem_prompt"].format(answer=self._answer),
            options_str,
            examples=examples_str if examples_str else None
        )

    def _create_additional_choices(self, num_options: int, mc_type: MathExpressionType) -> tuple[list[str], int]:
        if mc_type == MathExpressionType.MC_EVALUATE_PROBLEM:
            values = [self.answer]
        elif mc_type == MathExpressionType.MC_SELECT_PROBLEM:
            values = [self.problem]
        seed_increment: int = 1

        while len(values) < num_options:
            new_problem = MathExpressionResponseProblem(seed=self.seed + seed_increment)
            new_problem.generate(
                min_depth=self.min_depth,
                max_depth=self.max_depth,
                min_value=self.min_value,
                max_value=self.max_value,
                min_sub_expressions=self.min_sub_expressions,
                max_sub_expressions=self.max_sub_expressions
            )
            seed_increment += 1

            if mc_type == MathExpressionType.MC_EVALUATE_PROBLEM:
                if new_problem.answer != self.answer and new_problem.answer not in values:
                    values.append(new_problem.answer)
            elif mc_type == MathExpressionType.MC_SELECT_PROBLEM:
                if new_problem.problem != self.problem and new_problem.problem not in values:
                    values.append(new_problem.problem)

            """
            if mc_type == MathExpressionType.MC_EVALUATE_PROBLEM:
                if new_problem.problem != self.problem and new_problem.answer not in values:
                    values.append(new_problem.answer)
            elif mc_type == MathExpressionType.MC_SELECT_PROBLEM:
                if new_problem.answer != self.answer and new_problem.problem not in values:
                    values.append(new_problem.problem)
            """

        self.rng.shuffle(values)
        return values, seed_increment

    def _generate_examples_for_multiple_choice(
        self,
        num_shots: int,
        num_options: int, 
        use_uppercase: bool,
        use_lowercase: bool,
        use_numbers: bool,
        prevent_same_letter_case: bool,
        randomize: bool,
        seed_increment: int,
        include_evaluate_expression: bool = True, 
        include_select_expression: bool = True
    ) -> str:
        examples = []
        for i in range(num_shots):
            example_problem = MathExpressionMultipleChoiceProblem(
                seed=self.seed + seed_increment + i
            )
            example_problem.generate(
                min_depth=self.min_depth, 
                max_depth=self.max_depth, 
                min_value=self.min_value, 
                max_value=self.max_value, 
                min_sub_expressions=self.min_sub_expressions, 
                max_sub_expressions=self.max_sub_expressions
            )
            example_problem.generate_prompt(
                num_shots=0, 
                num_options=num_options, 
                use_uppercase=use_uppercase, 
                use_lowercase=use_lowercase, 
                use_numbers=use_numbers, 
                prevent_same_letter_case=prevent_same_letter_case, 
                randomize=randomize,
                include_evaluate_expression=include_evaluate_expression,
                include_select_expression=include_select_expression
            )
            examples.append(
                self.prompts["multiple_choice_example"].format(problem_prompt=example_problem.prompt, answer=example_problem.answer)
            )
        
        return "".join(example for example in examples)
