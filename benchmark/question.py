from benchmark.constraints.constraint import Constraint


class Question:
    def __init__(self, prompt: str = "", constraints: list[Constraint] = None, topic: str | None = None):
        self.prompt: str = prompt  # The question prompt
        self.constraints: list[Constraint] = constraints if constraints is not None else []  # Constraints the response must satisfy
        self.topic = topic # The topic of the question

    def generate_prompt(self, seed: int | None = None, use_llm: bool = False, llm_model: str = "llama3-70b-8192", temperature: float = 0.2, max_tokens: int = 8192, top_p: float = 0.95) -> None:
        def generate_llm_prompt() -> str:
            import json
            import os

            import dotenv
            import groq

            dotenv.load_dotenv()
            client: groq.GROQ = groq.Groq()

            model: str = "llama3-70b-8192"
            system_prompt: str = "You are an expert prompt engineer. You will be given a topic and a list of constraints. Your task is to generate a prompt that clearly communicates the topic and each of the constraints to a LLM. Do not make assumptions about the prompt, add information, or remove information. Provide only the generated prompt in your response, formatted as a JSON object with a single 'prompt' field. Do not attempt to generate a response to the prompt itself. E.g., {'prompt': 'Put your prompt here.'}"

            user_prompt: str = json.dumps({"topic": self.topic, "tasks": task_descriptions})

            # Groq does not use seed
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p
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

    def evaluate_response(self, response: str, seed: str | None = None) -> tuple[bool, list[str]]:
        def validate_topic_with_llm() -> bool:
            import json
            import math

            import dotenv
            import openai

            dotenv.load_dotenv()

            client: openai.OpenAI = openai.OpenAI()

            if seed is None:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"Is the given response about the topic {self.topic}? Respond only with 'Yes' or 'No'."},
                        {"role": "user", "content": response}
                    ],
                    logprobs=True,
                    top_logprobs=2,
                    logit_bias={9642: 100, 2822: 100}, # Adjust logit bias so 'Yes' and 'No' are extremely likely
                    max_tokens=1
                )
            else:
                completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Is the given response about the topic {self.topic}? Respond only with 'Yes' or 'No'."},
                    {"role": "user", "content": response}
                ],
                logprobs=True,
                top_logprobs=2,
                logit_bias={9642: 100, 2822: 100}, # Adjust logit bias so 'Yes' and 'No' are extremely likely
                max_tokens=1,
                seed=seed
            )

            model_completion: str = completion.choices[0].logprobs
            json_response: dict = json.loads(model_completion.json())
            top_logprobs: list[dict] = json_response["content"][0]["top_logprobs"]
            probabilities: list[float] = [math.exp(logprob["logprob"]) for logprob in top_logprobs]

            # If one option is the clear winner, return that
            if probabilities[0] > 0.95:
                return "yes" in top_logprobs[0]["token"].lower()

            # Otherwise, raise an error because it is unclear which option is correct
            import warnings
            warnings.warn(f"Unable to determine the validity of the topic '{self.topic}' with the given response: {response}. \nLogprobs: {top_logprobs}")

            # If we can't determine the validity, it is probably False
            return False

        # Check constraints
        violated_constraints_descriptions: list[str] = []
        num_all_constraints = len(self.constraints)
        num_valid_constraints = 0
        valid_constraints = [] # List of constraints that were satisfied
        for constraint in self.constraints:
            if not constraint.validate(response):
                violated_constraints_descriptions.extend(constraint.violations)
            else :
                num_valid_constraints += 1
                valid_constraints.append(constraint.description)
        partial_correctness = num_valid_constraints / num_all_constraints # Partial correctness score
        partial_correctness_string = "Out of {num_all_constraints} constraints, {num_valid_constraints} were satisfied, Partial Correctness Score = {partial_correctness}.".format(num_all_constraints = num_all_constraints, num_valid_constraints = num_valid_constraints, partial_correctness = partial_correctness)

        if not validate_topic_with_llm():
            violated_constraints_descriptions.append("The response does not match the given topic.")

        # Determine overall correctness based on the absence of constraint violations
        correctness: bool = len(violated_constraints_descriptions) == 0

        # Return evaluation result and any constraint violations descriptions
        return correctness, violated_constraints_descriptions, partial_correctness_string, valid_constraints 

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
