import json

from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem

class LiarProblem(BaseProblem):
    def __init__(self, seed: int | None = None, prompts: dict = None) -> None:
        super().__init__(seed)

        self.problem_name: str = "liar_problem"

        with open("utils/names.json") as f:
            self.names: list[str] = json.load(f)["names"]

        if not prompts:
            with open("benchmark/prompts/en/liar_problem_prompts.json", "r") as f:
                prompts = json.load(f)
        
        self.problem_prompt: str = prompts["problem_prompt"]
        self.multiple_choice_prompt_t: str = prompts["multiple_choice_prompt_t"]
        self.multiple_choice_prompt_f: str = prompts["multiple_choice_prompt_f"]

        self.truthfulness: dict[str, bool] = {}
        self.statements: list[str] = []
        self.final_truth: bool = False
        self.statement_style: bool = False
        
    def generate(self, num_people: int = 5) -> None:
        self.num_people = num_people
        self.names = self.rng.sample(self.names, num_people)
        self.truthfulness = {name: self.rng.choice([True, False]) for name in self.names}
        self.statement_style = self.rng.choice([True, False])
        
        self.statements.append(f"{self.names[0]} always {'tells the truth' if self.truthfulness[self.names[0]] else 'lies'}.")
        
        for i in range(1, num_people):
            previous_name = self.names[i - 1]
            current_name = self.names[i]
            
            if self.statement_style:  # Current about Previous
                if self.truthfulness[current_name]:
                    self.statements.append(f"{current_name} says {previous_name} {'tells the truth' if self.truthfulness[previous_name] else 'lies'}.")
                else:
                    self.statements.append(f"{current_name} says {previous_name} {'tells the truth' if not self.truthfulness[previous_name] else 'lies'}.")
            else:  # Previous about Current
                if self.truthfulness[previous_name]:
                    self.statements.append(f"{previous_name} says {current_name} {'tells the truth' if self.truthfulness[current_name] else 'lies'}.")
                else:
                    self.statements.append(f"{previous_name} says {current_name} {'tells the truth' if not self.truthfulness[current_name] else 'lies'}.")
        
        self.problem = " ".join(self.statements)
        self.answer = str(self.truthfulness[self.names[-1]])
        self.correct_answer = self.answer

class LiarResponseProblem(LiarProblem, ResponseProblem):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
    def generate_prompt(self, num_shots: int = 0) -> None:
        self.prompt = f"{self.problem_prompt}\n\n{self.problem}\n\nIs {self.names[-1]} telling the truth? Answer 'True' or 'False'."
        
        examples = []
        for i in range(num_shots):
            example_problem = LiarResponseProblem(seed=self.seed+i)
            example_problem.generate(self.num_people)
            example_problem.generate_prompt(num_shots=0)
            examples.append(f"{example_problem.prompt}\n{example_problem.answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"

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
        
        values = [" ".join(self.statements)]
        seed_increment: int = 1

        while len(values) < num_options:
            new_problem = LiarResponseProblem(seed=self.seed+seed_increment)
            new_problem.generate(self.num_people)
            seed_increment += 1

            if new_problem.answer != self.answer and new_problem.problem not in values:
                values.append(new_problem.problem)

        self.rng.shuffle(values)
        self.options = dict(zip(option_labels, values))
        self.option_labels = option_labels

        options_str = "\n".join([f"{label}. {option}" for label, option in zip(option_labels, values)])

        correct_label = next(label for label, option in self.options.items() if option == self.problem)
        self.correct_answer = correct_label

        if self.answer == "True":
            self.prompt = f"{self.multiple_choice_prompt_t}\n\n{options_str}"
        else:
            self.prompt = f"{self.multiple_choice_prompt_f}\n\n{options_str}"

        examples = []
        for i in range(num_shots):
            example_problem = LiarMultipleChoiceProblem(seed=self.seed + seed_increment + i)
            example_problem.generate(self.num_people)
            example_problem.generate_prompt(num_shots=0, num_options=num_options, use_uppercase=use_uppercase, use_lowercase=use_lowercase, use_numbers=use_numbers, prevent_same_letter_case=prevent_same_letter_case, randomize=randomize)
            examples.append(f"{example_problem.prompt}\n{example_problem.correct_answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"
