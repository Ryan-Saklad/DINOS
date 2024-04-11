import random
from typing import List

class LogicalDeductionProblem:
    def __init__(self) -> None:
        self.prompt: str = ""
        self.options: List[str] = []

    def generate(self) -> None:
        objects = ["animals", "fruits", "colors"]
        random.shuffle(objects)

        if objects[0] == "animals":
            self.generate_animals_problem()
        elif objects[0] == "fruits":
            self.generate_fruits_problem()
        elif objects[0] == "colors":
            self.generate_colors_problem()
        elif objects[0] == "golfers":
            self.generate_golfers_problem()

    def generate_golfers_problem() -> tuple[str, List[str]]:
        golfers = ["Rob", "Ada", "Dan", "Joe", "Mel"]
        random.shuffle(golfers)
        
        statements = [
            f"{golfers[1]} finished above {golfers[4]}.",
            f"{golfers[4]} finished above {golfers[2]}.",
            f"{golfers[3]} finished below {golfers[2]}.",
            f"{golfers[1]} finished second."
        ]

        random.shuffle(statements)

        prompt = "The following paragraphs each describe a set of five objects arranged in a fixed order. The statements are logically consistent within each paragraph.\n\n"
        prompt += "In a golf tournament, there were five golfers: "
        prompt += ", ".join(golfers) + ".\n"
        prompt += "\n".join(statements)
        options = [f"({chr(65+i)}) {golfer} finished second." for i, golfer in enumerate(golfers)]

        return prompt, options
    
    
    def generate_animals_problem(self) -> None:
        animals = ["lion", "tiger", "elephant", "giraffe", "zebra"]
        random.shuffle(animals)

        statements = [
            f"The {animals.index('lion')+1} is the fiercest.",
            f"The {animals.index('giraffe')+1} is taller than the {animals.index('elephant')+1}.",
            f"The {animals.index('tiger')+1} is to the left of the {animals.index('zebra')+1}.",
            f"The {animals.index('lion')+1} is the second from the left."
        ]

        random.shuffle(statements)

        self.prompt = "The following paragraphs each describe a set of five objects arranged in a fixed order. The statements are logically consistent within each paragraph.\n\n"
        self.prompt += "In a zoo, there are five animals: "
        self.prompt += ", ".join(animals) + ".\n"
        self.prompt += "\n".join(statements)
        self.options = [f"({chr(65+i)}) The {animals[i]} is the rightmost." for i in range(5)]

    def generate_fruits_problem(self) -> None:
        fruits = ["apple", "banana", "orange", "kiwi", "grape"]
        random.shuffle(fruits)

        statements = [
            f"The {fruits.index('banana')+1} is yellow.",
            f"The {fruits.index('orange')+1} is larger than the {fruits.index('apple')+1}.",
            f"The {fruits.index('kiwi')+1} is to the right of the {fruits.index('banana')+1}.",
            f"The {fruits.index('grape')+1} is the third from the left."
        ]

        random.shuffle(statements)

        self.prompt = "The following paragraphs each describe a set of five objects arranged in a fixed order. The statements are logically consistent within each paragraph.\n\n"
        self.prompt += "In a fruit basket, there are five fruits: "
        self.prompt += ", ".join(fruits) + ".\n"
        self.prompt += "\n".join(statements)
        self.options = [f"({chr(65+i)}) The {fruits[i]} is the second from the right." for i in range(5)]

    def generate_colors_problem(self) -> None:
        colors = ["red", "blue", "green", "yellow", "purple"]
        random.shuffle(colors)

        statements = [
            f"The {colors.index('red')+1} is the brightest.",
            f"The {colors.index('yellow')+1} is lighter than the {colors.index('green')+1}.",
            f"The {colors.index('blue')+1} is to the left of the {colors.index('purple')+1}.",
            f"The {colors.index('red')+1} is the fourth from the left."
        ]

        random.shuffle(statements)

        self.prompt = "The following paragraphs each describe a set of five objects arranged in a fixed order. The statements are logically consistent within each paragraph.\n\n"
        self.prompt += "In a spectrum, there are five colors: "
        self.prompt += ", ".join(colors) + ".\n"
        self.prompt += "\n".join(statements)
        self.options = [f"({chr(65+i)}) The {colors[i]} is the second-oldest." for i in range(5)]

    def display(self) -> None:
        print(self.prompt)
        print("\nOptions:")
        for option in self.options:
            print(option)