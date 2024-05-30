from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem


class BooleanExpressionProblem(BaseProblem):
    def __init__(self, seed: int | None = None, prompts: dict = None) -> None:
        super().__init__(seed)

        self.problem_name: str = "boolean_expression_problem"

        if not prompts:
            import json

            with open("benchmark/prompts/en/boolean_expression_problem_prompts.json", "r") as f:
                prompts = json.load(f)

        self.bool_values: list[str] = ["True", "False"]
        self.operators: list[str] = ["and", "or"]
        self.unary_operator: str = "not"
        
        self.problem_prompt: str = prompts["response_prompt"]
        self.multiple_choice_prompt_t: str = prompts["multiple_choice_prompt_t"]
        self.multiple_choice_prompt_f: str = prompts["multiple_choice_prompt_f"]

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

        self.problem: str = generate_expression(self.depth).replace("(True)", "True").replace("(False)", "False").replace("(not True)", "not True").replace("(not False)", "not False")
        self.answer: str = self._evaluate(self.problem)
        self.correct_answer: str = self.answer

    def _evaluate(self, expression: str) -> str:
        return str(eval(expression))

class BooleanExpressionResponseProblem(BooleanExpressionProblem, ResponseProblem):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def generate_prompt(self, num_shots: int = 0) -> None:
        self.prompt = f"{self.problem_prompt}\n\n{self.problem}"

        examples = []
        for i in range(num_shots):
            example_problem = BooleanExpressionResponseProblem(seed=seed+i)
            example_problem.generate(min_depth=self.depth, max_depth=self.depth)
            example_problem.generate_prompt(num_shots=0)
            examples.append(f"{example_problem.prompt}\n{example_problem.answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"


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
        
        values = [self.problem]
        seed_increment: int = 1

        while len(values) < num_options:
            new_problem = BooleanExpressionResponseProblem(seed=self.seed+seed_increment)
            new_problem.generate(min_depth=self.depth, max_depth=self.depth)
            seed_increment += 1

            if new_problem.answer != self.correct_answer and new_problem.problem not in values:
                values.append(new_problem.problem)

        self.rng.shuffle(values)
        self.options = dict(zip(option_labels, values))
        self.option_labels = option_labels

        options_str = "\n".join([f"{label}. {option}" for label, option in zip(option_labels, values)])

        correct_label = next(label for label, option in self.options.items() if option == self.problem)
        self.answer = correct_label

        if self.correct_answer == "True":
            self.prompt = f"{self.multiple_choice_prompt_t}\n\nOptions:\n{options_str}"
        else:
            self.prompt = f"{self.multiple_choice_prompt_f}\n\nOptions:\n{options_str}"

        examples = []
        for i in range(num_shots):
            example_problem = BooleanExpressionMultipleChoiceProblem(seed=self.seed + seed_increment + i)
            example_problem.generate(min_depth=self.depth, max_depth=self.depth)
            example_problem.generate_prompt(num_shots=0, num_options=num_options, use_uppercase=use_uppercase, use_lowercase=use_lowercase, use_numbers=use_numbers, prevent_same_letter_case=prevent_same_letter_case, randomize=randomize)
            examples.append(f"{example_problem.prompt}\n{example_problem.answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"
