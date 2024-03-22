from benchmark.constraints.element_count_constraint import ElementCountConstraint
from benchmark.constraints.element_frequency_constraint import ElementFrequencyConstraint
from benchmark.constraints.element_length_pattern_constraint import ElementLengthPatternConstraint
from benchmark.constraints.element_repetition_constraint import ElementRepetitionConstraint
from benchmark.constraints.fibonacci_sequence_constraint import FibonacciSequenceConstraint

from utils.element_type import ElementType
import random

element_types = [ElementType.WORDS, ElementType.CHARACTERS, ElementType.SENTENCES, ElementType.PARAGRAPHS]
def gather_constraints(seed, list_of_constraints) : 
    constraints = []
    def randomizer(seed) : 
        random.seed(seed)
        # Return a random number between 0 and 1
        return random.uniform(0, 1)
    # Randomly select constraints to add
    for constraint in list_of_constraints:
        if randomizer(seed) > 0.5:
            constraints.append(constraint)