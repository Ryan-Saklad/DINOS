from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem

class MathExpressionProblem(BaseProblem):
    def __init__(self, seed: int | None = None) -> None:
        super().__init__(seed)
        
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
        
        depth: int = self.rng.randint(min_depth, max_depth)
        num_sub_expressions: int = self.rng.randint(min_sub_expressions, max_sub_expressions)
        
        self.problem = generate_expression(depth, num_sub_expressions)
        self.answer = str(eval(self.problem))
        self.correct_answer = self.answer

class MathExpressionResponseProblem(MathExpressionProblem, ResponseProblem):
    def __init__(self, seed: int | None = None) -> None:
        super().__init__(seed)
        
        self.problem_prompt: str = "Please evaluate the following mathematical expression. Respond only with the numerical value."
        
    def generate_prompt(self, num_shots: int = 0) -> None:
        self.prompt = f"{self.problem_prompt}\n\n{self.problem}"
        
        examples = []
        for i in range(num_shots):
            example_problem = MathExpressionResponseProblem(seed=self.seed+i)
            example_problem.generate()
            example_problem.generate_prompt(num_shots=0)
            examples.append(f"{example_problem.prompt}\n{example_problem.answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"

class MathExpressionMultipleChoiceProblem(MathExpressionProblem, MultipleChoiceProblem):
    def __init__(self, seed: int | None = None) -> None:
        super().__init__(seed)
        
        self.multiple_choice_prompt: str = "Select the choice that correctly evaluates the following mathematical expression. Respond only with the label corresponding to your choice."

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
        
        values = [self.answer]
        seed_increment: int = 1

        while len(values) < num_options:
            new_problem = MathExpressionResponseProblem(seed=self.seed+seed_increment)
            new_problem.generate()
            seed_increment += 1

            if new_problem.answer != self.answer and new_problem.answer not in values:
                values.append(new_problem.answer)

        self.rng.shuffle(values)
        self.options = dict(zip(option_labels, values))
        self.option_labels = option_labels
        
        options_str = "\n".join([f"{label}. {option}" for label, option in zip(option_labels, values)])
        self.prompt = f"{self.multiple_choice_prompt}\n\n{self.problem}\n\nOptions:\n{options_str}"

        correct_label = next(label for label, option in self.options.items() if option == self.answer)
        self.correct_answer = correct_label

        examples = []
        for i in range(num_shots):
            example_problem = MathExpressionMultipleChoiceProblem(seed=self.seed + seed_increment + i)
            example_problem.generate()
            example_problem.generate_prompt_evaluate_expression(num_shots=0, num_options=num_options, use_uppercase=use_uppercase, use_lowercase=use_lowercase, use_numbers=use_numbers, prevent_same_letter_case=prevent_same_letter_case, randomize=randomize)
            examples.append(f"{example_problem.prompt}\n{example_problem.correct_answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"

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
        
        values = [self.problem]
        seed_increment: int = 1

        while len(values) < num_options:
            new_problem = MathExpressionResponseProblem(seed=self.seed+seed_increment)
            new_problem.generate()
            seed_increment += 1

            if new_problem.problem not in values and new_problem.answer != self.answer:
                values.append(new_problem.problem)

        self.rng.shuffle(values)
        self.options = dict(zip(option_labels, values))
        self.option_labels = option_labels

        options_str = "\n".join([f"{label}. {option}" for label, option in zip(option_labels, values)])
        self.prompt = f"Select the option that evaluates to {self.answer}. Respond only with the label corresponding to your choice.\n\nOptions:\n{options_str}"

        correct_label = next(label for label, option in self.options.items() if option == self.problem)
        self.correct_answer = correct_label

        examples = []
        for i in range(num_shots):
            example_problem = MathExpressionMultipleChoiceProblem(seed=self.seed + seed_increment + i)
            example_problem.generate()

            example_problem.generate_prompt_select_expression(num_shots=0, num_options=num_options, use_uppercase=use_uppercase, use_lowercase=use_lowercase, use_numbers=use_numbers, prevent_same_letter_case=prevent_same_letter_case, randomize=randomize)
            examples.append(f"{example_problem.prompt}\n{example_problem.correct_answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"