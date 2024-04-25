from benchmark.problems.problem import Problem
from utils.problem_type import ProblemType

class NavigateProblem(Problem):
    problem_type = ProblemType.PROBLEM
    def __init__(self) -> None:
        super().__init__()
        self.prompt: str = "After following each instruction, where do you end up? Provide your answer as a pair of coordinates (x, y), where you always face forward. "

    def generate(self, num_steps: int = 7, min_distance: int = 1, max_distance: int = 10) -> None:
        # Options: Take N step(s) forward/left/right/backwards, Turn left/right/around
        # E.g. Take 6 steps right. Take 1 step forward. Take 10 steps left. Take 8 steps forward. Take 9 steps backward. Take 4 steps right.

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

    def validate(self, response: str) -> bool:
        fmt_response = self.strip_boilerplate(response)
        return fmt_response.lower() == self.answer.lower()
