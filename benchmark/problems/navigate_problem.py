from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class NavigateProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "navigate_problem"
        super().__init__(**kwargs)

    def generate(self, min_num_steps: int = 5, max_num_steps: int = 7, min_distance: int = 1, max_distance: int = 10, **kwargs) -> None:
        directions = ["forward", "left", "right", "backward"]
        turns = ["left", "right", "around"]
        actions = []

        self.min_num_steps: int = min_num_steps
        self.max_num_steps: int = max_num_steps
        self.num_steps = self.config.rng.randint(min_num_steps, max_num_steps)
        self.min_distance: int = min_distance
        self.max_distance: int = max_distance

        x, y = 0, 0  # Starting position
        facing = 0  # 0: North, 1: East, 2: South, 3: West

        for _ in range(self.num_steps):
            action_type = self.config.rng.choice(["move", "turn"])

            if action_type == "move":
                direction = self.config.rng.choice(directions)
                steps = self.config.rng.randint(min_distance, max_distance)
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
                turn = self.config.rng.choice(turns)
                action = f"Turn {turn}."
                actions.append(action)

                if turn == "left":
                    facing = (facing - 1) % 4
                elif turn == "right":
                    facing = (facing + 1) % 4
                elif turn == "around":
                    facing = (facing + 2) % 4

        self.problem: str = " ".join(actions)
        self._answer: str = f"({x}, {y})"
        self.answer: str = self._answer


class NavigateResponseProblem(NavigateProblem, ResponseProblem):
    pass


class NavigateMultipleChoiceProblem(NavigateProblem, MultipleChoiceProblem):
    def generate_prompt(self, **kwargs) -> None:
        if ProblemType.CHOOSE_MATCHING_EXPRESSION not in self.problem_types:
            self.problem_types.append(ProblemType.CHOOSE_MATCHING_EXPRESSION)
        super().generate_prompt(**kwargs)

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
            new_problem = NavigateResponseProblem(config=self.config)
            new_problem.generate(min_num_steps=self.num_steps, max_num_steps=self.num_steps, min_distance=self.min_distance, max_distance=self.max_distance)

            if new_problem._answer != self._answer and new_problem.problem not in [option.problem for label, option in option_pairs if option is not None]:
                problems.append(new_problem)

        for i, (label, option) in enumerate(option_pairs):
            if option is None and problems:
                option_pairs[i] = (label, problems.pop(0))

        return option_pairs, correct_label
