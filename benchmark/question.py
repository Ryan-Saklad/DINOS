from benchmark.constraints.constraint import Constraint


class Question:
    def __init__(self, prompt: str = "", constraints: list[Constraint] = None):
        self.prompt: str = prompt  # The question prompt
        self.constraints: list[Constraint] = constraints if constraints is not None else []  # Constraints the response must satisfy

    def generate_prompt(self) -> None:
        task_descriptions: list[str] = [constraint.description for constraint in self.constraints]
        self.prompt = "Please generate a response that satisfies the following constraints: " + "; ".join(task_descriptions)

    def evaluate_response(self, response: str) -> dict[str, list[Constraint] | bool]:
        # Evaluate the LLM's response against the constraints
        # This is a simplified example. Real evaluation would be more complex.

        # Check constraints
        constraint_violations: list[Constraint] = []
        for constraint in self.constraints:
            if not constraint.validate(response):
                constraint_violations.append(constraint)

        # Determine overall correctness based on the absence of constraint violations
        correctness: bool = len(constraint_violations) == 0

        # Return evaluation result and any constraint violations
        return {"correctness": correctness, "violations": constraint_violations}

    def provide_feedback(self, evaluation_result: dict[str, list[Constraint] | bool]) -> str:
        # Generate feedback based on the evaluation of the response
        feedback: list[str] = []
        if evaluation_result['correctness']:
            feedback.append("Your response meets all the constraints.")
        else: # TODO: Add more detailed feedback for incorrectness
            feedback.append("Your response violated the following constraints:")
            for violation in evaluation_result['violations']:
                feedback.append(f"- {violation.description}")

        return "\n".join(feedback)
