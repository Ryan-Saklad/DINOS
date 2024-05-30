import argparse
import json
import random

from tqdm import tqdm

from benchmark.problems.problem import BaseProblem
from utils.problem_type import ProblemType

from benchmark.problems.boolean_expression_problem import BooleanExpressionResponseProblem, BooleanExpressionMultipleChoiceProblem
from benchmark.problems.dyck_language_problem import DyckLanguageResponseProblem, DyckLanguageMultipleChoiceProblem
from benchmark.problems.liar_problem import LiarResponseProblem, LiarMultipleChoiceProblem
from benchmark.problems.math_expression_problem import MathExpressionResponseProblem, MathExpressionMultipleChoiceProblem
from benchmark.problems.navigate_problem import NavigateResponseProblem, NavigateMultipleChoiceProblem

problem_classes: list = [
    BooleanExpressionResponseProblem, 
    BooleanExpressionMultipleChoiceProblem, 
    DyckLanguageResponseProblem, 
    DyckLanguageMultipleChoiceProblem, 
    LiarResponseProblem, 
    LiarMultipleChoiceProblem, 
    MathExpressionResponseProblem, 
    MathExpressionMultipleChoiceProblem, 
    NavigateResponseProblem, 
    NavigateMultipleChoiceProblem
]

def generate_benchmark(seed: int | None = None, num_problems: int = 1000) -> dict[str, list[dict]]:
    SEED_MULTIPLIER: int = 1000000  # Problems sometimes iterate through seeds and this avoids collisions
    problems: list[dict] = []

    if seed is None:
        seed = random.randint(0, 1000000)

    for i in range(num_problems):
        problem_seed: int = seed + i * SEED_MULTIPLIER
        random.seed(problem_seed)
        problem = random.choice(problem_classes)(seed=problem_seed)
        problem.generate()
        problem.generate_prompt()
        problem_json: dict = problem.generate_problem_json()
        problem_json['problem_seed'] = problem_seed
        problems.append(problem_json)

    return {"seed": seed, "problems": problems}

def save_benchmark(benchmark: dict, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(benchmark, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Generate a DINOS benchmark.")
    parser.add_argument('--seed', type=int, help='Seed for random number generator', default=None)
    parser.add_argument('--num_problems', type=int, help='Number of problems to generate', default=1000)
    parser.add_argument('--output', type=str, help='Output file path', default='benchmark.json')
    
    args = parser.parse_args()

    benchmark = generate_benchmark(seed=args.seed, num_problems=args.num_problems)
    save_benchmark(benchmark, args.output)

if __name__ == '__main__':
    main()
