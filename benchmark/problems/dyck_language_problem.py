from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class DyckLanguageProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "dyck_language_problem"
        super().__init__(**kwargs)

        self.parens: list[tuple[str, str]] = [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]

    def generate(self, min_length: int = 5, max_length: int = 10) -> None:
        self.min_length: int = min_length
        self.max_length: int = max_length
        self.length: int = self.config.rng.randint(min_length, max_length)

        def generate_dyck_word(length: int) -> str:
            if length == 0:
                return ""
            else:
                split = self.config.rng.randint(0, length - 1)
                left = generate_dyck_word(split)
                right = generate_dyck_word(length - split - 1)
                paren = self.config.rng.choice(self.parens)
                return f"{paren[0]}{left}{right}{paren[1]}"
        
        def valid_split_index(dyck_word: str) -> int:
            last_start_index = -1
            for i, char in enumerate(dyck_word):
                if char in "([{<":
                    last_start_index = i
            return last_start_index + 1 if last_start_index != -1 else len(dyck_word) // 2

        dyck_word = generate_dyck_word(self.length // 2 * 2)  # Ensure even length

        split_index = valid_split_index(dyck_word)
        random_split_index = self.config.rng.randint(split_index, len(dyck_word) - 1)

        self.problem = dyck_word[:random_split_index]
        self._answer = dyck_word[random_split_index:]
        self.answer = self._answer


class DyckLanguageResponseProblem(DyckLanguageProblem, ResponseProblem):
    def generate_prompt(self, num_shots: int = 0) -> None:
        self.prompt: str = self.render_template(examples=self._generate_examples(num_shots))

    def _generate_examples(self, num_shots: int) -> list[ResponseProblem]:
        examples = []
        for i in range(num_shots):
            self.config.increment_seed()
            example_problem = DyckLanguageResponseProblem(config=self.config)
            example_problem.generate(min_length=self.length, max_length=self.length)
            example_problem.generate_prompt(num_shots=0)
            examples.append(example_problem)

        return examples


class DyckLanguageMultipleChoiceProblem(DyckLanguageProblem, MultipleChoiceProblem):
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

        self.problem_types.append(ProblemType.SOLVE_EXPRESSION)

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
            new_problem = DyckLanguageResponseProblem(config=self.config)
            new_problem.generate(min_length=self.length, max_length=self.length)

            if new_problem._answer != self._answer and new_problem.problem not in [option.problem for label, option in option_pairs if option is not None]:
                problems.append(new_problem)

        for i, (label, option) in enumerate(option_pairs):
            if option is None and problems:
                option_pairs[i] = (label, problems.pop(0))

        return option_pairs, correct_label

    def _generate_examples(self, num_shots: int) -> list[ResponseProblem]:
        examples = []
        for i in range(num_shots):
            self.config.increment_seed()
            example_problem = DyckLanguageMultipleChoiceProblem(config=self.config)
            example_problem.generate(min_length=self.length, max_length=self.length)
            example_problem.generate_prompt(num_shots=0)
            examples.append(example_problem)

        return examples
