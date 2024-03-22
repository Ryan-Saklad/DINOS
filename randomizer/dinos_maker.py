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
random_word_list = word_list = ["apple", "book", "desk", "pen", "cat", "dog", "tree", "house", "car", "phone",
             "computer", "laptop", "keyboard", "mouse", "chair", "table", "door", "window", "wall", "floor"]

def make_prompts(seed, list_of_prompts = []) : 
    constraint_gatherer.set_seed(seed)
    constraints = constraint_gatherer.gather_constraints(initial_constraints)
    for i in constraints : 
        if type(i) == ElementCountConstraint : 
            element_type = random.choice(element_types)
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
            case_sensitive = random.choice(case_sensitive)
            current_constraint = ElementCountConstraint(element_type, element, min_count, max_count, exact_count, case_sensitive)
        elif type(i) == ElementFrequencyConstraint : 
            element_type = random.choice(element_types)
            element = random.choice(random_word_list)
            choice = constraint_gatherer.randomizer()
            if choice > 0.5 : 
                min_frequency = random.uniform(0, 1)
            choice = constraint_gatherer.randomizer()
            if choice > 0.5 : 
                max_frequency = min(min_frequency + random.uniform(0, 1), 1)
            case_sensitive = random.choice(case_sensitive)
            current_constraint = ElementFrequencyConstraint(element_type, element, min_frequency, max_frequency, case_sensitive)
        elif type(i) == ElementLengthPatternConstraint : 
            element_type = random.choice([ElementType.WORDS, ElementType.SENTENCES])
            scope_type = random.choice([ElementType.SENTENCES, ElementType.PARAGRAPHS])
            increasing = random.choice([True, False])
            choice = constraint_gatherer.randomizer()
            if choice > 0.5 : 
                min_length_diff = random.randint(1, 50)
            else : 
                min_length_diff = 1
            current_constraint = ElementLengthPatternConstraint(element_type, scope_type, increasing, min_length_diff)
        elif type(i) == ElementRepetitionConstraint : 
            element_type = random.choice([ElementType.CHARACTERS, ElementType.WORDS])
            element = random.choice(random_word_list)
            choice = constraint_gatherer.randomizer()
            if choice > 0.5 : 
                scope_type = ElementType.PARAGRAPHS
            else : 
                scope_type = ElementType.SENTENCES
            case_sensitive = random.choice(case_sensitive)
            choice = constraint_gatherer.randomizer()
            if choice > 0.5 : 
                min_repetitions = random.randint(1, 100)
            else : 
                min_repetitions = None
            choice = constraint_gatherer.randomizer()
            if choice > 0.5 : 
                max_repetitions = min_repetitions + random.randint(1, 50)
            else : 
                max_repetitions = None
            current_constraint = ElementRepetitionConstraint(element_type, element, min_repetitions, max_repetitions, scope_type, case_sensitive)
        elif type(i) == FibonacciSequenceConstraint :
            element_type = random.choice(element_types)
            current_constraint = FibonacciSequenceConstraint(element_type)

make_prompts(42)