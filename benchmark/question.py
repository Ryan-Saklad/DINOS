from benchmark.constraints.constraint import Constraint


class Question:
    def __init__(self, prompt: str = "", constraints: list[Constraint] = None, topic = "Anything"):
        self.prompt: str = prompt  # The question prompt
        self.constraints: list[Constraint] = constraints if constraints is not None else []  # Constraints the response must satisfy
        self.topic = topic # The topic of the question

    def generate_prompt(self) -> None:
        task_descriptions: list[str] = [constraint.description for constraint in self.constraints]
        self.prompt = "Please generate a response that satisfies the following constraints: " + "Topic: {topic}".format(topic = self.topic) + "; " + "; ".join(task_descriptions)

    def evaluate_response(self, response: str) -> tuple[bool, list[str]]:
        # Evaluate the LLM's response against the constraints

        # Check constraints
        violated_constraints_descriptions: list[str] = []
        num_all_constraints = len(self.constraints)
        num_valid_constraints = 0
        for constraint in self.constraints:
            if not constraint.validate(response):
                violated_constraints_descriptions.extend(constraint.violations)
            else :
                num_valid_constraints += 1
        partial_correctness = num_valid_constraints / num_all_constraints
        partial_correctness_string = "Out of {num_all_constraints} constraints, {num_valid_constraints} were satisfied, Partial Correctness Score = {partial_correctness}.".format(num_all_constraints = num_all_constraints, num_valid_constraints = num_valid_constraints, partial_correctness = partial_correctness)

        # Determine overall correctness based on the absence of constraint violations
        correctness: bool = len(violated_constraints_descriptions) == 0

        # Return evaluation result and any constraint violations descriptions
        return correctness, violated_constraints_descriptions, partial_correctness_string

    def provide_feedback(self, evaluation_result: tuple[bool, list[str]]) -> str:
        # Generate feedback based on the evaluation of the response
        feedback: list[str] = []
        if evaluation_result[0]:
            feedback.append("Your response meets all the constraints.")
        else: # TODO: Add more detailed feedback for incorrectness
            feedback.append("Your response violated the following constraints:")
            for violation_description in evaluation_result[1]:
                feedback.append(f"- {violation_description}")

        return "\n".join(feedback)
