from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem

class DyckLanguageProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "dyck_language_problem"
        super().__init__(**kwargs)

        self.parens: list[tuple[str, str]] = [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]

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

        self._problem = dyck_word[:random_split_index]
        self._answer = dyck_word[random_split_index:]
        self.problem = self._problem
        self.answer = self._answer


class DyckLanguageResponseProblem(DyckLanguageProblem, ResponseProblem):
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
            example_problem = DyckLanguageResponseProblem(seed=self.seed + i)
            example_problem.generate()
            example_problem.generate_prompt(num_shots=0)
            examples.append(self.prompts["response_example"].format(problem_prompt=example_problem.prompt, answer=example_problem.answer))
        
        return "".join(example for example in examples)


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
        
        values, seed_increment = self._create_additional_choices(num_options)

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
            seed_increment
        )

        self.generate_multiple_choice_prompt(
            self.prompts["multiple_choice_problem_prompt"],
            options_str,
            examples=examples_str if examples_str else None
        )

    def _create_additional_choices(self, num_options: int) -> tuple[list[str], int]:
        values = [self.answer]
        seed_increment: int = 1

        while len(values) < num_options:
            new_problem = DyckLanguageResponseProblem(seed=self.seed + seed_increment)
            new_problem.generate()
            seed_increment += 1

            if new_problem.answer != self.answer and new_problem.answer not in values:
                values.append(new_problem.answer)

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
        seed_increment: int
    ) -> str:
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
            examples.append(self.prompts["multiple_choice_example"].format(
                problem_prompt=example_problem.prompt, 
                answer=example_problem.answer
            ))
        
        return "".join(examples)
