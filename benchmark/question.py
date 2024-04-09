from benchmark.constraints.constraint import Constraint


class Question:
    def __init__(self, prompt: str = "", constraints: list[Constraint] = None, topic: str | None = None):
        self.prompt: str = prompt  # The question prompt
        self.constraints: list[Constraint] = constraints if constraints is not None else []  # Constraints the response must satisfy
        self.topic = topic # The topic of the question

    def generate_prompt(self, seed: int | None = None, use_llm: bool = False) -> None:
        def generate_llm_prompt() -> str:
            import json
            import os

            import dotenv
            import openai

            dotenv.load_dotenv()

            client: openai.types.chat.chat_completion.ChatCompletion = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            prompt: str = """
            Generate a prompt for an AI language model that will cause it to generate a response that satisfies all of the following user-supplied constraints.
            Be sure to include each constraint verbatim in the generated prompt. Do not include other information in the prompt, such as a topic or story that is not given.
            Provide only the generated prompt in your response, formatted as a JSON object with a single 'prompt' field.
            Do not attempt to generate a response to the prompt itself.
            """

            if self.topic:
                constraints: str = f"{self.topic}\n- " + "\n- ".join(task_descriptions)
            else:
                constraints: str = "\n- ".join(task_descriptions)
                
            messages: list[dict[str, str]] = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": constraints},
            ]
            
            if seed is None:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    response_format={"type": "json_object"},
                    messages=messages,
                )
            else:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    response_format={"type": "json_object"},
                    messages=messages,
                    seed=seed,
                )

            prompt_json: dict[str, str] = json.loads(response.choices[0].message.content)
            prompt: str = prompt_json["prompt"]

            return prompt

        task_descriptions: list[str] = [constraint.description for constraint in self.constraints]

        if use_llm:
            self.prompt = generate_llm_prompt()
        elif self.topic is None:
            self.prompt = "Please generate a response that satisfies the following constraints:\n- " + "\n- ".join(task_descriptions)
        else:
            self.prompt = "Please generate a response that satisfies the following constraints:\n- Topic: {topic}\n- ".format(topic=self.topic) + "\n- ".join(task_descriptions)

    def evaluate_response(self, response: str) -> tuple[bool, list[str]]:
        # Evaluate the LLM's response against the constraints

        # Check constraints
        violated_constraints_descriptions: list[str] = []
        for constraint in self.constraints:
            if not constraint.validate(response):
                violated_constraints_descriptions.extend(constraint.violations)

        # Determine overall correctness based on the absence of constraint violations
        correctness: bool = len(violated_constraints_descriptions) == 0

        # Return evaluation result and any constraint violations descriptions
        return correctness, violated_constraints_descriptions

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
