from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem

class NavigateProblem(BaseProblem):
    def __init__(self, seed: int | None = None, prompts: dict = None) -> None:
        super().__init__(seed)

        self.problem_name: str = "navigate_problem"

        if not prompts:
            import json

            with open("benchmark/prompts/en/navigate_problem_prompts.json", "r") as f:
                prompts = json.load(f)
        
        self.problem_prompt: str = prompts["problem_prompt"]
        self.multiple_choice_prompt_answer: str = prompts["multiple_choice_prompt_answer"]

    def generate(self, num_steps: int = 7, min_distance: int = 1, max_distance: int = 10) -> None:
        directions = ["forward", "left", "right", "backward"]
        turns = ["left", "right", "around"]
        actions = []

        x, y = 0, 0  # Starting position
        facing = 0  # 0: North, 1: East, 2: South, 3: West

        for _ in range(num_steps):
            action_type = self.rng.choice(["move", "turn"])

            if action_type == "move":
                direction = self.rng.choice(directions)
                steps = self.rng.randint(min_distance, max_distance)
                action = f"Take {steps} step{'s' if steps > 1 else ''} {direction}."
                actions.append(action)

                if direction == "forward":
                    if facing == 0: y += steps
                    elif facing == 1: x += steps 
                    elif facing == 2: y -= steps
                    elif facing == 3: x -= steps
                elif direction == "backward":
                    if facing == 0: y -= steps
                    elif facing == 1: x -= steps
                    elif facing == 2: y += steps
                    elif facing == 3: x += steps
                elif direction == "left":
                    if facing == 0: x -= steps
                    elif facing == 1: y += steps
                    elif facing == 2: x += steps
                    elif facing == 3: y -= steps
                elif direction == "right":
                    if facing == 0: x += steps
                    elif facing == 1: y -= steps
                    elif facing == 2: x -= steps
                    elif facing == 3: y += steps
            else:
                turn = self.rng.choice(turns)
                action = f"Turn {turn}."
                actions.append(action)

                if turn == "left":
                    facing = (facing - 1) % 4
                elif turn == "right":
                    facing = (facing + 1) % 4
                elif turn == "around":
                    facing = (facing + 2) % 4

        self.problem = " ".join(actions)
        self.answer = f"({x}, {y})"
        self.correct_answer = self.answer

class NavigateResponseProblem(NavigateProblem, ResponseProblem):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
    def generate_prompt(self, num_shots: int = 0) -> None:
        self.prompt = f"{self.problem_prompt}\n\n{self.problem}"
        
        examples = []
        for i in range(num_shots):
            example_problem = NavigateResponseProblem(seed=self.seed+i)
            example_problem.generate()
            example_problem.generate_prompt(num_shots=0)
            examples.append(f"{example_problem.prompt}\n{example_problem.answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"

class NavigateMultipleChoiceProblem(NavigateProblem, MultipleChoiceProblem):
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
        randomize: bool = False,
        include_problem_prompt: bool = True, 
        include_answer_prompt: bool = True
    ) -> None:
        if include_problem_prompt and include_answer_prompt:
            if self.rng.choice([True, False]):
                self.generate_prompt_problem(num_shots, num_options, use_uppercase, use_lowercase, use_numbers, prevent_same_letter_case, randomize)
            else:
                self.generate_prompt_answer(num_shots, num_options, use_uppercase, use_lowercase, use_numbers, prevent_same_letter_case, randomize)
        elif include_problem_prompt:
            self.generate_prompt_problem(num_shots, num_options, use_uppercase, use_lowercase, use_numbers, prevent_same_letter_case, randomize)
        elif include_answer_prompt:
            self.generate_prompt_answer(num_shots, num_options, use_uppercase, use_lowercase, use_numbers, prevent_same_letter_case, randomize)
        else:
            raise ValueError("At least one of include_problem_prompt or include_answer_prompt must be True")

    def generate_prompt_problem(
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
            new_problem = NavigateResponseProblem(seed=self.seed+seed_increment)
            new_problem.generate()
            seed_increment += 1

            if new_problem.problem not in values and new_problem.answer != self.answer:
                values.append(new_problem.problem)

        self.rng.shuffle(values)
        self.options = dict(zip(option_labels, values))
        self.option_labels = option_labels

        options_str = "\n".join([f"{label}. {option}" for label, option in zip(option_labels, values)])
        self.prompt = f"Select the choice that contains the instructions that lead to the given final coordinates, {self.answer}, where you always face forward. Respond only with the label corresponding to your choice.\n\nOptions:\n{options_str}"

        correct_label = next(label for label, option in self.options.items() if option == self.problem)
        self.correct_answer = correct_label

        examples = []
        for i in range(num_shots):
            example_problem = NavigateMultipleChoiceProblem(seed=self.seed + seed_increment + i)
            example_problem.generate()

            example_problem.generate_prompt_problem(num_shots=0, num_options=num_options, use_uppercase=use_uppercase, use_lowercase=use_lowercase, use_numbers=use_numbers, prevent_same_letter_case=prevent_same_letter_case, randomize=randomize)
            examples.append(f"{example_problem.prompt}\n{example_problem.correct_answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"

    def generate_prompt_answer(
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
            new_problem = NavigateResponseProblem(seed=self.seed+seed_increment)
            new_problem.generate()
            seed_increment += 1

            if new_problem.answer != self.answer and new_problem.answer not in values:
                values.append(new_problem.answer)

        self.rng.shuffle(values)
        self.options = dict(zip(option_labels, values))
        self.option_labels = option_labels
        
        options_str = "\n".join([f"{label}. {option}" for label, option in zip(option_labels, values)])
        self.prompt = f"{self.multiple_choice_prompt_answer}\n\n{self.problem}\n\nOptions:\n{options_str}"

        correct_label = next(label for label, option in self.options.items() if option == self.answer)
        self.correct_answer = correct_label

        examples = []
        for i in range(num_shots):
            example_problem = NavigateMultipleChoiceProblem(seed=self.seed + seed_increment + i)
            example_problem.generate()
            example_problem.generate_prompt_answer(num_shots=0, num_options=num_options, use_uppercase=use_uppercase, use_lowercase=use_lowercase, use_numbers=use_numbers, prevent_same_letter_case=prevent_same_letter_case, randomize=randomize)
            examples.append(f"{example_problem.prompt}\n{example_problem.correct_answer}")
        
        examples_str = "\n\n".join(examples)
        
        if len(examples) > 0:
            self.prompt = f"{examples_str}\n\n{self.prompt}"
