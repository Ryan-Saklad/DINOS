from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem


class BooleanExpressionProblem(BaseProblem):
    def __init__(self, seed: int | None = None, prompts: dict = None) -> None:
        self.problem_name: str = "boolean_expression_problem"

        super().__init__(seed)

        if prompts is not None:
            self.prompts.update(prompts)

        self.bool_values: list[str] = ["True", "False"]
        self.operators: list[str] = ["and", "or"]
        self.unary_operator: str = "not"

    def generate(self, min_depth: int = 3, max_depth: int = 4) -> None:
        if min_depth < 1 or max_depth < min_depth:
            raise ValueError("min_depth must be >= 1 and max_depth must be >= min_depth")

        self.depth = self.rng.randint(min_depth, max_depth)

        def generate_expression(depth: int) -> str:
            if depth == 1:
                return self.rng.choice(self.bool_values)
            else:
                sub_expr1 = generate_expression(depth - 1)
                sub_expr2 = generate_expression(depth - 1)

                # Randomly choose to use a unary operator or a binary operator
                if self.rng.random() < 0.5:
                    return f"{self.unary_operator} ({sub_expr1})"
                else:
                    operator = self.rng.choice(self.operators)
                    return f"({sub_expr1}) {operator} ({sub_expr2})"

        self._problem: str = generate_expression(self.depth)
        self._answer: str = self._evaluate(self._problem)

        self.generate_problem_str()
        self.generate_answer_str()

    def generate_problem_str(self) -> None:
        self.problem = (
            self._problem
            .replace("True", self.prompts["true_value"])
            .replace("False", self.prompts["false_value"])
            .replace("and", self.prompts["and_value"])
            .replace("or", self.prompts["or_value"])
            .replace("not", self.prompts["not_value"])
            .replace("(", self.prompts["start_parenthesis_value"])
            .replace(")", self.prompts["end_parenthesis_value"])
        )

    def generate_answer_str(self) -> None:
        self.answer: str = (
            self._answer
            .replace("True", self.prompts["true_value"])
            .replace("False", self.prompts["false_value"])
            .replace("and", self.prompts["and_value"])
            .replace("or", self.prompts["or_value"])
            .replace("not", self.prompts["not_value"])
            .replace("(", self.prompts["start_parenthesis_value"])
            .replace(")", self.prompts["end_parenthesis_value"])
        )

    def _evaluate(self, expression: str) -> str:
        return str(eval(expression))


class BooleanExpressionResponseProblem(BooleanExpressionProblem, ResponseProblem):
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
            example_problem = BooleanExpressionResponseProblem(seed=self.seed + i)
            example_problem.generate(min_depth=self.depth, max_depth=self.depth)
            example_problem.generate_prompt(num_shots=0)
            examples.append(f"{example_problem.prompt}\n{example_problem.answer}")
        
        return "\n\n".join([self.prompts["response_example"].format(example=example) for example in examples])


class BooleanExpressionMultipleChoiceProblem(BooleanExpressionProblem, MultipleChoiceProblem):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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
        
        values, seed_increment = self._create_additional_choices(num_options)
        self.rng.shuffle(values)
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
            seed_increment
        )
        
        self.generate_multiple_choice_prompt(
            self.prompts["multiple_choice_problem_prompt_t"] if self._answer == "True" else self.prompts["multiple_choice_problem_prompt_f"],
            options_str,
            examples=examples_str if examples_str else None
        )

    def _create_additional_choices(self, num_options: int) -> tuple[list[str], int]:
        values = [self.problem]
        seed_increment: int = 1

        while len(values) < num_options:
            new_problem = BooleanExpressionResponseProblem(seed=self.seed + seed_increment)
            new_problem.generate(min_depth=self.depth, max_depth=self.depth)
            seed_increment += 1

            if new_problem._answer != self._answer and new_problem.problem not in values:
                values.append(new_problem.problem)

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
        seed_increment: int
    ) -> str:
        examples = []
        for i in range(num_shots):
            example_problem = BooleanExpressionMultipleChoiceProblem(
                seed=self.seed + seed_increment + i
            )
            example_problem.generate(
                min_depth=self.depth, max_depth=self.depth
            )
            example_problem.generate_prompt(
                num_shots=0, 
                num_options=num_options, 
                use_uppercase=use_uppercase, 
                use_lowercase=use_lowercase, 
                use_numbers=use_numbers, 
                prevent_same_letter_case=prevent_same_letter_case, 
                randomize=randomize
            )
            examples.append(
                f"{example_problem.prompt}\n{example_problem._answer}"
            )
        
        return "\n\n".join([self.prompts["multiple_choice_example"].format(example=example) for example in examples])
