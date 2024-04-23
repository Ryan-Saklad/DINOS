from utils.element_type import ElementType
from utils.output_type import OutputType
from randomizer import constraint_gatherer
from benchmark.constraints.element_count_constraint import ElementCountConstraint
from benchmark.constraints.element_frequency_constraint import ElementFrequencyConstraint
from benchmark.constraints.element_length_pattern_constraint import ElementLengthPatternConstraint
from benchmark.constraints.element_repetition_constraint import ElementRepetitionConstraint
from benchmark.constraints.fibonacci_sequence_constraint import FibonacciSequenceConstraint
from benchmark.constraints.isogram_constraint import IsogramConstraint
from benchmark.constraints.output_format_constraint import OutputFormatConstraint
from benchmark.constraints.palindrome_constraint import PalindromeConstraint
from benchmark.constraints.write_backwards_constraint import WriteBackwardsConstraint
from benchmark.problems.boolean_expression_problem import BooleanExpressionProblem
from benchmark.problems.dyck_language_problem import DyckLanguageProblem
from benchmark.problems.liar_problem import LiarProblem
from benchmark.problems.math_expression_problem import MathExpressionProblem
from benchmark.problems.navigate_problem import NavigateProblem
from benchmark import question
import random

initial_constraints = [ElementCountConstraint, ElementFrequencyConstraint, ElementLengthPatternConstraint, ElementRepetitionConstraint, FibonacciSequenceConstraint, IsogramConstraint
                       , OutputFormatConstraint, PalindromeConstraint, WriteBackwardsConstraint, BooleanExpressionProblem, DyckLanguageProblem, LiarProblem, MathExpressionProblem, NavigateProblem]
element_types = [ElementType.WORDS, ElementType.CHARACTERS, ElementType.SENTENCES, ElementType.PARAGRAPHS]
count_type = ["exact_count", "range_count"]
case_sensitive = [True, False]
random_word_list = [
    "house", "run", "book", "jump", "car", "sing", "dog", "play",
    "ball", "write", "bike", "read", "cat", "swim", "tree", "eat",
    "friend", "talk", "school", "draw", "sun", "dance", "game", "cook",
    "bird", "walk", "sleep", "work", "flower", "love", "help", "laugh",
    "music", "watch", "story", "build", "rain", "learn", "smile", "grow",
    "water", "think", "ride", "color", "dream", "see" 
]
char_list = [chr(i) for i in range(97, 123)]
topics = [
    "vegetables", "cheese", "banking", "hammocks", "basketball", 
    "games", "meteorology", "tattoos", "barbers", "pork", 
    "coffin", "farmers markets", "weaving", "Central America", 
    "dentistry", "post office", "alligators", "boats", "pineapple", 
    "royalty", "windmills", "cotton", "playing cards", "seashells", 
    "flood", "giants", "Disney movies", "money", "military", 
    "shipwrecks", "postcards", "coins", "gorillas", "camels", 
    "firemen", "veterinarians", "athletics", "banana", "slavery", 
    "sailing", "football", "pipe organs", "communism", "Africa",
    "skull", "vaccines", "accordions", "beekeeping", "cats", 
    "paper boys", "balloons", "potatoes", "bears", "spinning", 
    "magicians", "World War 1", "Europe", "buffaloes", "smoking",
    "Salvation Army", "criminals", "pipes", "spas", "bread", 
    "Red Cross", "insects", "zeppelins", "drugstores", "South America",
    "parachuting", "shells", "giraffes", "baseball", "frogs", 
    "boxing", "lions", "motorcycles", "sewing machines", "hunting", 
    "earthquake", "pottery", "printing", "masonry", "justice", 
    "rice", "mountaineering", "pilots", "hotels", "music", 
    "fencing", "bridges", "rugby", "journalism", "shoes", 
    "snakes", "engineering", "horses", "cards", "spiritism", "cemetery"
]


def make_prompts(seed, num_prompts = 1, topic = False, num_per_prompt = -1, constraint_type = None, llm = False) : 
    constraint_gatherer.set_seed(seed)
    prompts = []
    prompts_object = []
    for num_runs in range(num_prompts) : 
        current_constraint = None
        constraints = constraint_gatherer.gather_constraints(initial_constraints, num_constraints = num_per_prompt, constraint_type = constraint_type)
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
                    if element_type == ElementType.WORDS :
                        min_count = random.randint(1, 5)
                        max_count = min_count + random.randint(1, 10)
                    else :
                        min_count = random.randint(1, 25)
                        max_count = min_count + random.randint(1, 25)
                    exact_count = None
                else : 
                    min_count = None
                    max_count = None
                    if element_type == ElementType.WORDS :
                        exact_count = random.randint(1, 15)
                    else :
                        exact_count = random.randint(1, 75)
                case_sensitive_choice = random.choice(case_sensitive)
                current_constraint = ElementCountConstraint(element_type, element, min_count, max_count, exact_count, case_sensitive_choice)
            elif i == ElementFrequencyConstraint : 
                element_type = random.choice(element_types)
                element = random.choice(random_word_list)
                choice = constraint_gatherer.randomizer()
                if choice > 0.5 : 
                    min_frequency = round(random.uniform(0, 0.25) * 100, 0)
                    max_frequency = round(min(min_frequency + random.uniform(0, 0.50), 1)* 100, 0) # max frequency is at most 100, calculated as min + random number between 0 and 1   
                elif choice >= 0.25 : 
                    min_frequency = None
                    max_frequency = round(random.uniform(0, 0.50) * 100, 0)
                else : 
                    min_frequency = round(random.uniform(0, 0.25) * 100, 0)
                    max_frequency = None
                case_sensitive_choice = random.choice(case_sensitive)
                current_constraint = ElementFrequencyConstraint(element_type, element, min_frequency, max_frequency, case_sensitive_choice)
            elif i == ElementLengthPatternConstraint: 
                element_type = random.choice([ElementType.WORDS, ElementType.SENTENCES])
                scope_type = random.choice([ElementType.SENTENCES, ElementType.PARAGRAPHS])
                increasing = random.choice([True, False])
                choice = constraint_gatherer.randomizer()
                if choice > 0.5 : 
                    if element_type == ElementType.WORDS :
                        min_length_diff = random.randint(1, 10)
                    else :
                        min_length_diff = random.randint(1, 25)
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
                    if element_type == ElementType.WORDS :
                        min_repetitions = random.randint(1, 5)
                        max_repetitions = min_repetitions + random.randint(1, 10)
                    else :
                        min_repetitions = random.randint(1, 25)
                        max_repetitions = min_repetitions + random.randint(1, 25)
                elif choice >= 0.25 : 
                    min_repetitions = None
                    if element_type == ElementType.WORDS :
                        max_repetitions = random.randint(1, 15)
                    else :
                        max_repetitions = random.randint(1, 50)
                else : 
                    if element_type == ElementType.WORDS :
                        min_repetitions = random.randint(1, 15)
                    else :
                        min_repetitions = random.randint(1, 50)
                    max_repetitions = None
                current_constraint = ElementRepetitionConstraint(element_type, element, min_repetitions, max_repetitions, scope_type, case_sensitive_choice)
            elif i == FibonacciSequenceConstraint:
                element_type = random.choice(element_types)
                current_constraint = FibonacciSequenceConstraint(element_type)
            elif i == IsogramConstraint: 
                current_constraint = IsogramConstraint()
            elif i == OutputFormatConstraint:
                wrap_text = ""
                output_type = random.choice([OutputType.JSON, OutputType.YAML, OutputType.XML, OutputType.WRAP])
                wrap_lines = random.randint(1, 5)
                if output_type == OutputType.WRAP:
                    wrap_text = random.choice(["###", "$$$", "!!!", "&&&"])
                current_constraint = OutputFormatConstraint(output_type, wrap_text, wrap_lines)
            elif i == PalindromeConstraint:
                current_constraint = PalindromeConstraint()
            elif i == WriteBackwardsConstraint:
                current_constraint = WriteBackwardsConstraint()
            
            elif i == BooleanExpressionProblem:
                min_depth = random.randint(2, 5)
                max_depth = random.randint(min_depth, 7)
                problem = BooleanExpressionProblem()
                problem.generate(min_depth, max_depth)
                prompt = problem.prompt + problem.problem
            elif i == DyckLanguageProblem:
                min_length = random.randint(5, 10)
                max_length = random.randint(min_length, 15)
                problem = DyckLanguageProblem()
                problem.generate(min_length, max_length)
                prompt = problem.prompt + problem.problem
            elif i == LiarProblem:
                num_people = random.randint(3, 7)
                problem = LiarProblem()
                problem.generate(num_people)
                prompt = problem.prompt + problem.problem
            elif i == MathExpressionProblem:
                min_depth = random.randint(2, 3)
                max_depth = random.randint(min_depth, 4)
                min_value = random.randint(-9, 9)
                max_value = random.randint(min_value, 9)
                min_sub_expressions = random.randint(2, 4)
                max_sub_expressions = random.randint(min_sub_expressions, 5)
                problem = MathExpressionProblem()
                problem.generate(min_depth, max_depth, min_value, max_value, min_sub_expressions, max_sub_expressions)
                prompt = problem.prompt + problem.problem
            elif i == NavigateProblem:
                num_steps = random.randint(5, 10)
                min_distance = random.randint(1, 5)
                max_distance = random.randint(min_distance, 10)
                problem = NavigateProblem()
                problem.generate(num_steps, min_distance, max_distance)
                prompt = problem.prompt + problem.problem

            if current_constraint : 
                single_run_prompts.append(current_constraint)
        if topic and single_run_prompts : 
            q = question.Question(constraints= single_run_prompts, topic = random.choice(topics))
        elif single_run_prompts : 
            q = question.Question(constraints= single_run_prompts)
        if single_run_prompts :
            q.generate_prompt(seed=seed, use_llm=llm)
            prompts.append((q.prompt, constraint_type))
            prompts_object.append(q)
        else : 
            prompts.append((prompt, constraint_type))
            prompts_object.append(problem)
    return prompts, prompts_object