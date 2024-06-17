import argparse
import json
import random

from tqdm import tqdm

from benchmark.problems.problem import BaseProblem
from utils.problem_type import ProblemType
from benchmark.config import Config

from benchmark.problems.boolean_expression_problem import BooleanExpressionResponseProblem, BooleanExpressionMultipleChoiceProblem
from benchmark.problems.dyck_language_problem import DyckLanguageResponseProblem, DyckLanguageMultipleChoiceProblem
# from benchmark.problems.liar_problem import LiarResponseProblem, LiarMultipleChoiceProblem
# from benchmark.problems.math_expression_problem import MathExpressionResponseProblem, MathExpressionMultipleChoiceProblem
from benchmark.problems.navigate_problem import NavigateResponseProblem, NavigateMultipleChoiceProblem

problem_classes: list = [
    # BooleanExpressionResponseProblem, 
    # BooleanExpressionMultipleChoiceProblem, 
    DyckLanguageResponseProblem, 
    DyckLanguageMultipleChoiceProblem, 
    # LiarResponseProblem, 
    # LiarMultipleChoiceProblem, 
    # MathExpressionResponseProblem, 
    # MathExpressionMultipleChoiceProblem, 
    # NavigateResponseProblem, 
    # NavigateMultipleChoiceProblem
]

def generate_benchmark(seed: int | None = None, num_problems: int = 1000, max_problem_types: int = None, num_shots: int = 0) -> dict[str, dict]:
    SEED_MULTIPLIER: int = 1000000  # Problems sometimes iterate through seeds and this avoids collisions
    problems: dict = {}

    config = Config(seed=seed)

    selected_problem_classes = problem_classes
    if max_problem_types is not None:
        selected_problem_classes = random.sample(problem_classes, min(max_problem_types, len(problem_classes)))

    for i in range(num_problems):
        config.increment_seed()
        problem = config.rng.choice(selected_problem_classes)(config=config)
        problem.generate()
        problem.generate_prompt(num_shots=num_shots)
        problem_json: dict = problem.generate_problem_json(i)
        problem_key = next(iter(problem_json))  # Get the first (and only) key from the dictionary
        problems[problem_key] = problem_json[problem_key]

    return {"seed": config.seed, "problems": problems}

def save_benchmark(benchmark: dict, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(benchmark, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Generate a DINOS benchmark.")
    parser.add_argument('--seed', type=int, help='Seed for random number generator', default=None)
    parser.add_argument('--num_problems', type=int, help='Number of problems to generate', default=1000)
    parser.add_argument('--output', type=str, help='Output file path', default='benchmark.json')
    parser.add_argument('--max_problem_types', type=int, help='Maximum number of types of problems to include', default=None)
    parser.add_argument('--num_shots', type=int, help='Number of example problems to include in the prompt', default=0)
    
    args = parser.parse_args()

    benchmark = generate_benchmark(seed=args.seed, num_problems=args.num_problems, max_problem_types=args.max_problem_types, num_shots=args.num_shots)
    save_benchmark(benchmark, args.output)

if __name__ == '__main__':
    main()
