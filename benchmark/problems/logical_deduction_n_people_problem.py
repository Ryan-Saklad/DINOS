import json
import warnings
from itertools import permutations

from benchmark.problems.problem import BaseProblem, ResponseProblem, MultipleChoiceProblem
from utils.problem_type import ProblemType


class LogicalDeductionNPeopleProblem(BaseProblem):
    def __init__(self, **kwargs) -> None:
        self.problem_name: str = "logical_deduction_n_people"
        super().__init__(**kwargs)

        with open("utils/names.json") as f:
            self.names: list[str] = json.load(f)["names"]

        self.problems: dict[str, BaseProblem] = {
            "response": LogicalDeductionNPeopleResponseProblem,
            "multiple_choice": LogicalDeductionNPeopleMultipleChoiceProblem
        }
        self.statements: list[str] = []

        self.unmentioned_person: str = ""

    def generate(self, num_people: int = 5, **kwargs) -> None:
        if num_people > 7:
            warnings.warn("This uses a factorial algorithm, so it may take a long time to generate for large num_people.")

        self.num_people = num_people
        self.names = self.config.rng.sample(self.names, num_people)

        self.unmentioned_person = self.config.rng.choice(self.names)

        for index, person in enumerate(self.names):
            if person == self.unmentioned_person:
                continue

            statement_choices: list[str] = []

            if index == 0:
                statement_choices.append(f"{person} is the leftmost person.")
            if index == self.num_people - 1:
                statement_choices.append(f"{person} is the rightmost person.")

            if index != 0:
                statement_choices.append(f"{person} is to the right of {self.names[index - 1]}.")
            if index != self.num_people - 1:
                statement_choices.append(f"{person} is to the left of {self.names[index + 1]}.")
            if 0 < index < self.num_people - 1:
                statement_choices.append(f"{person} is between {self.names[index - 1]} and {self.names[index + 1]}.")

                left_position = index + 1
                right_position = self.num_people - index

                statement_choices.append(f"{person} is {left_position} positions from the left.")
                statement_choices.append(f"{person} is {right_position} positions from the right.")

            self.statements.append(self.config.rng.choice(statement_choices))

        if not self._evaluate():
            self.config.increment_seed()
            self.__init__(**vars(self))
            self.generate(num_people=num_people)
            return

        self.problem: str = " ".join(self.config.rng.sample(self.statements, len(self.statements)))
        self._answer: str = self.names.index(self.unmentioned_person) + 1  # The unmentioned person's position
        self.answer: str = self._answer

    def _evaluate(self) -> bool:
        remaining_people: set = set(self.names)

        guarenteed_people_order = ["?" for _ in range(self.num_people)]

        for constraint in self.statements:
            if " is the leftmost person." in constraint:
                person = constraint.split(" is the leftmost person.")[0]
                remaining_people.remove(person)
                guarenteed_people_order[0] = person
            elif " is the rightmost person." in constraint:
                person = constraint.split(" is the rightmost person.")[0]
                remaining_people.remove(person)
                guarenteed_people_order[-1] = person
            elif " positions from the left." in constraint:
                parts = constraint.split(" is ")
                person = parts[0]
                position = int(parts[1].split(" positions from the left.")[0])
                guarenteed_people_order[position - 1] = person
                remaining_people.remove(person)
            elif " positions from the right." in constraint:
                parts = constraint.split(" is ")
                person = parts[0]
                position = int(parts[1].split(" positions from the right.")[0])
                guarenteed_people_order[-position] = person
                remaining_people.remove(person)

            if len(remaining_people) == 1:
                return True

        # Second round of checking for constraints that can be inferred 
        updated = True
        while updated:
            updated = False
            for constraint in self.statements:
                if " is to the left of " in constraint:
                    left_person = constraint.split(" is to the left of ")[0]
                    right_person = constraint.split(" is to the left of ")[1].split(".")[0]
                    
                    if not left_person in guarenteed_people_order or not right_person in guarenteed_people_order:
                        continue
                    elif left_person in guarenteed_people_order and not right_person in guarenteed_people_order:
                        remaining_people.remove(right_person)
                        guarenteed_people_order[guarenteed_people_order.index(left_person) + 1] = right_person
                        updated = True
                    elif not left_person in guarenteed_people_order and right_person in guarenteed_people_order:
                        remaining_people.remove(left_person)
                        guarenteed_people_order[guarenteed_people_order.index(right_person) - 1] = left_person
                        updated = True
                elif " is to the right of " in constraint:
                    right_person = constraint.split(" is to the right of ")[0]
                    left_person = constraint.split(" is to the right of ")[1].split(".")[0]
                    
                    if not left_person in guarenteed_people_order or not right_person in guarenteed_people_order:
                        continue
                    elif left_person in guarenteed_people_order and not right_person in guarenteed_people_order:
                        remaining_people.remove(right_person)
                        guarenteed_people_order[guarenteed_people_order.index(left_person) - 1] = right_person
                        updated = True
                    elif not left_person in guarenteed_people_order and right_person in guarenteed_people_order:
                        remaining_people.remove(left_person)
                        guarenteed_people_order[guarenteed_people_order.index(right_person) + 1] = left_person
                        updated = True
                elif " is between " in constraint:
                    left_person = constraint.split(" is between ")[0]
                    right_person = constraint.split(" is between ")[1].split(" and ")[1].split(".")[0]
                    middle_person = constraint.split(" is between ")[1].split(" and ")[0]
                    
                    if not left_person in guarenteed_people_order or not right_person in guarenteed_people_order or not middle_person in guarenteed_people_order:
                        continue
                    elif left_person in guarenteed_people_order and not right_person in guarenteed_people_order:
                        remaining_people.remove(right_person)
                        guarenteed_people_order[guarenteed_people_order.index(left_person) + 1] = right_person
                        updated = True
                    elif not left_person in guarenteed_people_order and right_person in guarenteed_people_order:
                        remaining_people.remove(left_person)
                        guarenteed_people_order[guarenteed_people_order.index(right_person) - 1] = left_person
                        updated = True
                    elif left_person in guarenteed_people_order and not middle_person in guarenteed_people_order:
                        remaining_people.remove(middle_person)
                        guarenteed_people_order[guarenteed_people_order.index(left_person) + 1] = middle_person
                        updated = True
                    elif not left_person in guarenteed_people_order and middle_person in guarenteed_people_order:
                        remaining_people.remove(left_person)
                        guarenteed_people_order[guarenteed_people_order.index(middle_person) - 1] = left_person
                        updated = True
                    elif middle_person in guarenteed_people_order and not right_person in guarenteed_people_order:
                        remaining_people.remove(right_person)
                        guarenteed_people_order[guarenteed_people_order.index(middle_person) + 1] = right_person
                        updated = True
                    elif not middle_person in guarenteed_people_order and right_person in guarenteed_people_order:
                        remaining_people.remove(middle_person)
                        guarenteed_people_order[guarenteed_people_order.index(right_person) - 1] = middle_person
                        updated = True

        all_possible_orders = self._get_all_permutations(guarenteed_people_order, remaining_people)
        for order in all_possible_orders:
            if order == guarenteed_people_order:
                continue
            if self._is_valid_permutation(order):
                return False
        return True

    def _get_all_permutations(self, guarenteed_people_order, remaining_people):
        # Replaces '?' with remaining names in all possible permutations
        question_mark_indices = [i for i, x in enumerate(guarenteed_people_order) if x == "?"]
        all_permutations = []
        for perm in permutations(remaining_people):
            temp_order = list(guarenteed_people_order)
            for idx, person in zip(question_mark_indices, perm):
                temp_order[idx] = person
            all_permutations.append(temp_order)
        return all_permutations

    def _is_valid_permutation(self, permutation):
        for constraint in self.statements:
            if " is to the left of " in constraint:
                left_person = constraint.split(" is to the left of ")[0]
                right_person = constraint.split(" is to the left of ")[1].split(".")[0]
                if permutation.index(left_person) > permutation.index(right_person):
                    return False
            elif " is to the right of " in constraint:
                right_person = constraint.split(" is to the right of ")[0]
                left_person = constraint.split(" is to the right of ")[1].split(".")[0]
                if permutation.index(left_person) > permutation.index(right_person):
                    return False
            elif " is between " in constraint:
                left_person = constraint.split(" is between ")[0]
                right_person = constraint.split(" is between ")[1].split(" and ")[1].split(".")[0]
                middle_person = constraint.split(" is between ")[1].split(" and ")[0]
                if permutation.index(left_person) > permutation.index(middle_person) or \
                        permutation.index(middle_person) > permutation.index(right_person):
                    return False
        return True


class LogicalDeductionNPeopleResponseProblem(LogicalDeductionNPeopleProblem, ResponseProblem):
    pass


class LogicalDeductionNPeopleMultipleChoiceProblem(LogicalDeductionNPeopleProblem, MultipleChoiceProblem):
    def generate_prompt(self, **kwargs) -> None:
        super().generate_prompt(ProblemType.SOLVE_EXPRESSION, **kwargs)

    def _create_additional_choices(self, option_labels: list[str], num_options: int) -> tuple[list[tuple[str, ResponseProblem]], str, int]:
        if num_options > self.num_people:
            raise ValueError("Number of options can't be greater than or equal to num_people.")
    
        option_pairs: list[tuple[str, ResponseProblem]] = [(label, None) for label in option_labels]

        # Set the correct answer to this problem to a random label
        random_label = self.config.rng.choice([label for label, option in option_pairs if option is None])
        for i, (label, option) in enumerate(option_pairs):
            if label == random_label:
                option_pairs[i] = (label, self)
                correct_label = label
                break
        
        used_answers = [self._answer]
        problems = []
        while len(problems) < num_options:
            new_problem = self.__class__(**self.__dict__)
            new_problem._answer = self.config.rng.choice([i for i in range(1, self.num_people + 1) if i not in used_answers])
            used_answers.append(new_problem._answer)
            problems.append(new_problem)

        for i, (label, option) in enumerate(option_pairs):
            if option is None and problems:
                option_pairs[i] = (label, problems.pop(0))

        return option_pairs, correct_label

    def generate_problem_json(self, problem_id: int | None = None) -> dict:
        problem_json = super().generate_problem_json(problem_id)
        problem_json.update({
            "options": self.options,
            "answer": self.answer
        })

        return problem_json
