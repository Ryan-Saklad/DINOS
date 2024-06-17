from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class NavigateProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "navigate_problem"
        super().__init__(**kwargs)

        self.problems: dict[str, BaseProblem] = {
            "response": NavigateResponseProblem,
            "multiple_choice": NavigateMultipleChoiceProblem
        }

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
        super().generate_prompt(ProblemType.CHOOSE_MATCHING_EXPRESSION, **kwargs)
