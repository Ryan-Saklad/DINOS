import random

class ReverseTextProblem:
    def __init__(self) -> None:
        self.prompt: str = "Please write the following text backwards:"
        self.text: str = ""
        self.answer: str = ""

    def generate(self, text: str) -> None:
        self.text = text
        self.answer = text[::-1]

    def display(self) -> None:
        print(self.prompt)
        print(self.text)

    def validate(self, response: str) -> bool:
        return response == self.answer