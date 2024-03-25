from utils.element_type import ElementType
from randomizer import constraint_gatherer
from benchmark.constraints.element_count_constraint import ElementCountConstraint
from benchmark.constraints.element_frequency_constraint import ElementFrequencyConstraint
from benchmark.constraints.element_length_pattern_constraint import ElementLengthPatternConstraint
from benchmark.constraints.element_repetition_constraint import ElementRepetitionConstraint
from benchmark.constraints.fibonacci_sequence_constraint import FibonacciSequenceConstraint
from benchmark import question
import random

initial_constraints = [ElementCountConstraint, ElementFrequencyConstraint, ElementLengthPatternConstraint, ElementRepetitionConstraint, FibonacciSequenceConstraint]
element_types = [ElementType.WORDS, ElementType.CHARACTERS, ElementType.SENTENCES, ElementType.PARAGRAPHS]
count_type = ["exact_count", "range_count"]
case_sensitive = [True, False]
random_word_list = ["apple", "book", "desk", "pen", "cat", "dog", "tree", "house", "car", "phone",
             "computer", "laptop", "keyboard", "mouse", "chair", "table", "door", "window", "wall", "floor"]
char_list = [chr(i) for i in range(97, 123)]

def make_prompts(seed, list_of_prompts = [], num_prompts = 1) : 
    constraint_gatherer.set_seed(seed)
    prompts = []
    for num_runs in range(num_prompts) : 
        constraints = constraint_gatherer.gather_constraints(initial_constraints)
        single_run_prompts = []
        for i in constraints : 
            if i == ElementCountConstraint : 
                element_type = random.choice([ElementType.WORDS, ElementType.CHARACTERS])
                if element_type == ElementType.CHARACTERS :
                    element = random.choice(char_list)
                else : 
                    element = random.choice(random_word_list)
                choice = constraint_gatherer.randomizer()
                if choice > 0.5 : 
                    min_count = random.randint(1, 100)
                    max_count = min_count + random.randint(1, 50)
                    exact_count = None
                else : 
                    min_count = None
                    max_count = None
                    exact_count = random.randint(1, 100)
                case_sensitive_choice = random.choice(case_sensitive)
                current_constraint = ElementCountConstraint(element_type, element, min_count, max_count, exact_count, case_sensitive_choice)
            elif i == ElementFrequencyConstraint : 
                element_type = random.choice(element_types)
                element = random.choice(random_word_list)
                choice = constraint_gatherer.randomizer()
                if choice > 0.5 : 
                    min_frequency = round(random.uniform(0, 1) * 100, 0)
                    max_frequency = round(min(min_frequency + random.uniform(0, 1), 1)* 100, 0)
                elif choice >= 0.25 : 
                    min_frequency = None
                    max_frequency = round(random.uniform(0, 1) * 100, 0)
                else : 
                    min_frequency = round(random.uniform(0, 1) * 100, 0)
                    max_frequency = None
                case_sensitive_choice = random.choice(case_sensitive)
                current_constraint = ElementFrequencyConstraint(element_type, element, min_frequency, max_frequency, case_sensitive_choice)
            elif i == ElementLengthPatternConstraint: 
                element_type = random.choice([ElementType.WORDS, ElementType.SENTENCES])
                scope_type = random.choice([ElementType.SENTENCES, ElementType.PARAGRAPHS])
                increasing = random.choice([True, False])
                choice = constraint_gatherer.randomizer()
                if choice > 0.5 : 
                    min_length_diff = random.randint(1, 50)
                else : 
                    min_length_diff = 1
                current_constraint = ElementLengthPatternConstraint(element_type, scope_type, increasing, min_length_diff)
            elif i == ElementRepetitionConstraint: 
                element_type = random.choice([ElementType.CHARACTERS, ElementType.WORDS])
                if element_type == ElementType.CHARACTERS :
                    element = random.choice(char_list)
                else : 
                    element = random.choice(random_word_list)
                choice = constraint_gatherer.randomizer()
                if choice > 0.5 : 
                    scope_type = ElementType.PARAGRAPHS
                else : 
                    scope_type = ElementType.SENTENCES
                case_sensitive_choice = random.choice(case_sensitive)
                choice = constraint_gatherer.randomizer()
                if choice > 0.5 : 
                    min_repetitions = random.randint(1, 100)
                    max_repetitions = min_repetitions + random.randint(1, 50)
                elif choice >= 0.25 : 
                    min_repetitions = None
                    max_repetitions = random.randint(1, 100)
                else : 
                    min_repetitions = random.randint(1, 100)
                    max_repetitions = None
                current_constraint = ElementRepetitionConstraint(element_type, element, min_repetitions, max_repetitions, scope_type, case_sensitive_choice)
            elif i == FibonacciSequenceConstraint:
                element_type = random.choice(element_types)
                current_constraint = FibonacciSequenceConstraint(element_type)
            single_run_prompts.append(current_constraint)
        q = question.Question(constraints= single_run_prompts)
        q.generate_prompt()
        prompts.append(q.prompt)
    return prompts

print(make_prompts(42, num_prompts = 5)[1])