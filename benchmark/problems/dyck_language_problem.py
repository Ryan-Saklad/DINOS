from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem

class DyckLanguageProblem(BaseProblem):
    def __init__(self, seed: int | None = None, prompts: dict = None) -> None:
        super().__init__(seed)

        self.problem_name: str = "Dyck Language Problem"

        if not prompts:
            import json

            with open("benchmark/prompts/en/dyck_language_problem_prompts.json", "r") as f:
                prompts = json.load(f)

        self.parens: list[tuple[str, str]] = [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]

        self.problem_prompt: str = prompts["problem_prompt"]
        self.multiple_choice_prompt: str = prompts["multiple_choice_prompt"]

    def generate(self, min_length: int = 5, max_length: int = 10) -> None:
        def generate_dyck_word(length: int) -> str:
            if length == 0:
                return ""
            else:
                split = self.rng.randint(0, length - 1)
                left = generate_dyck_word(split)
                right = generate_dyck_word(length - split - 1)
                paren = self.rng.choice(self.parens)
                return f"{paren[0]}{left}{right}{paren[1]}"
        
        def valid_split_index(dyck_word: str) -> int:
            last_start_index = -1
            for i, char in enumerate(dyck_word):
                if char in "([{<":
                    last_start_index = i
            return last_start_index + 1 if last_start_index != -1 else len(dyck_word) // 2

        length: int = self.rng.randint(min_length, max_length)
        dyck_word = generate_dyck_word(length // 2 * 2)  # Ensure even length

        split_index = valid_split_index(dyck_word)
        random_split_index = self.rng.randint(split_index, len(dyck_word) - 1)
        self.problem = dyck_word[:random_split_index]
        self.answer = dyck_word[random_split_index:]

        self.correct_answer: str = self.answer

class DyckLanguageResponseProblem(DyckLanguageProblem, ResponseProblem):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def generate_prompt(self, num_shots: int = 0) -> None:
        self.prompt = f"{self.problem_prompt}\n\n{self.problem}"

        examples = []
        for i in range(num_shots):
            example_problem = DyckLanguageResponseProblem(seed=self.seed+i)
            example_problem.generate()
            example_problem.generate_prompt(num_shots=0)
            examples.append(f"{example_problem.prompt}\n{example_problem.answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"

class DyckLanguageMultipleChoiceProblem(DyckLanguageProblem, MultipleChoiceProblem):
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
        
        values = [self.correct_answer]
        seed_increment: int = 1

        while len(values) < num_options:
            new_problem = DyckLanguageResponseProblem(seed=self.seed+seed_increment)
            new_problem.generate()
            seed_increment += 1

            if new_problem.answer != self.answer and new_problem.answer not in values:
                values.append(new_problem.answer)

        self.rng.shuffle(values)

        self.options = {label: value for label, value in zip(option_labels, values)}
        self.option_labels = option_labels

        options_str = "\n".join([f"{label}. {option}" for label, option in zip(option_labels, values)])
        self.prompt = f"{self.multiple_choice_prompt}\n\n{self.problem}\n\nOptions:\n{options_str}"

        # Find the label corresponding to the correct answer
        correct_label = next(label for label, value in self.options.items() if value == self.correct_answer)
        self.correct_answer = correct_label

        examples = []
        for i in range(num_shots):
            example_problem = DyckLanguageMultipleChoiceProblem(seed=self.seed + seed_increment + i)
            example_problem.generate()
            example_problem.generate_prompt(
                num_shots=0, 
                num_options=num_options, 
                use_uppercase=use_uppercase, 
                use_lowercase=use_lowercase, 
                use_numbers=use_numbers, 
                prevent_same_letter_case=prevent_same_letter_case, 
                randomize=randomize
            )
            examples.append(f"{example_problem.prompt}\n{example_problem.correct_answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"
