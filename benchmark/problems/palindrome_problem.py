import random, string

class RandomPalindromeProblem:
    def __init__(self) -> None:
        self.prompt: str = "Is the following sequence of characters a palindrome?"
        self.sequence: str = ""
        self.answer: str = ""

    def generate(self, length: int) -> None:
        self.sequence = ''.join(random.choices(string.ascii_lowercase, k=length))
        self.answer = "Yes" if self.sequence == self.sequence[::-1] else "No"

    def display(self) -> None:
        print(self.prompt)
        print(self.sequence)

    def validate(self, response: str) -> bool:
        return response.lower() == self.answer.lower()