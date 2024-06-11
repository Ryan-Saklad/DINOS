import json

from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem

class LiarProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "liar_problem"
        super().__init__(**kwargs)

        with open("utils/names.json") as f:
            self.names: list[str] = json.load(f)["names"]

        self.truthfulness: dict[str, bool] = {}
        self.statements: list[str] = []
        self.final_truth: bool = False
        self.statement_style: bool = False
        
    def generate(self, num_people: int = 5) -> None:
        self.num_people = num_people
        self.names = self.rng.sample(self.names, num_people)
        self.truthfulness = {name: self.rng.choice([True, False]) for name in self.names}
        self.statement_style = self.rng.choice([True, False])
        
        if self.truthfulness[self.names[0]]:
            self.statements.append(self.prompts["begin_truthful_statement"].format(name=self.names[0]))
        else:
            self.statements.append(self.prompts["begin_lie_statement"].format(name=self.names[0]))
        
        for i in range(1, num_people):
            previous_name = self.names[i - 1]
            current_name = self.names[i]
            
            if self.statement_style:  # Current about Previous
                if self.truthfulness[current_name]:
                    if self.truthfulness[previous_name]:
                        self.statements.append(self.prompts["truthful_statement"].format(current_name=current_name, previous_name=previous_name))
                    else:
                        self.statements.append(self.prompts["liar_statement"].format(current_name=current_name, previous_name=previous_name))
                else:
                    if self.truthfulness[previous_name]:
                        self.statements.append(self.prompts["liar_statement"].format(current_name=current_name, previous_name=previous_name))
                    else:
                        self.statements.append(self.prompts["truthful_statement"].format(current_name=current_name, previous_name=previous_name))
            else:  # Previous about Current
                if self.truthfulness[previous_name]:
                    if self.truthfulness[current_name]:
                        self.statements.append(self.prompts["truthful_statement"].format(current_name=previous_name, previous_name=current_name))
                    else:
                        self.statements.append(self.prompts["liar_statement"].format(current_name=previous_name, previous_name=current_name))
                else:
                    if self.truthfulness[current_name]:
                        self.statements.append(self.prompts["liar_statement"].format(current_name=previous_name, previous_name=current_name))
                    else:
                        self.statements.append(self.prompts["truthful_statement"].format(current_name=previous_name, previous_name=current_name))

        self._problem = " ".join(self.statements)
        self._answer = str(self.truthfulness[self.names[-1]])
        self.problem = self._problem
        self.answer = self.prompts["true_value"] if self._answer == "True" else self.prompts.get("false_value", self._answer)


class LiarResponseProblem(LiarProblem, ResponseProblem):
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
            example_problem = LiarResponseProblem(seed=self.seed + i)
            example_problem.generate(self.num_people)
            example_problem.generate_prompt(num_shots=0)
            examples.append(self.prompts["response_example"].format(problem_prompt=example_problem.prompt, answer=example_problem.answer))
        
        return "".join(examples)

class LiarMultipleChoiceProblem(LiarProblem, MultipleChoiceProblem):
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

        if self._answer == "True":
            self.generate_multiple_choice_prompt(
                self.prompts["multiple_choice_problem_prompt_t"],
                options_str,
                examples=examples_str if examples_str else None
            )
        else:
            self.generate_multiple_choice_prompt(
                self.prompts["multiple_choice_problem_prompt_f"],
                options_str,
                examples=examples_str if examples_str else None
            )

    def _create_additional_choices(self, num_options: int) -> tuple[list[str], int]:
        values = [self.problem]
        seed_increment: int = 1

        while len(values) < num_options:
            new_problem = LiarResponseProblem(seed=self.seed + seed_increment)
            new_problem.generate(self.num_people)
            seed_increment += 1

            if new_problem._answer != self._answer and new_problem.problem not in values:
                values.append(new_problem.problem)

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
            example_problem = LiarMultipleChoiceProblem(seed=self.seed + seed_increment + i)
            example_problem.generate(self.num_people)
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
