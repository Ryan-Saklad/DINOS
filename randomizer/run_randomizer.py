import argparse
from randomizer import dinos_maker
import pandas as pd
import json
from utils.problem_type import ProblemType

parser = argparse.ArgumentParser(description='Generate random prompts for the Dinos Maker')
parser.add_argument('--num_prompts', type=int, default=1, help='Number of prompts to generate')
parser.add_argument('--topic', action='store_true', help='Include a topic in the prompt or let the model decide')
parser.add_argument('--seed', type=int, default=None, help='Seed for random number generator')
parser.add_argument('--output', type=str, default='random_prompts.json', help='Output file path for the prompts')
parser.add_argument('--num_per_prompt', type=int, default=-1, help='Number of constraints per prompt, defaults to no limit')
parser.add_argument('--constraint_type', type=str, default=[], nargs="*", help='Type of constraint to generate, defaults to random', choices = list(ProblemType.__members__.keys()))
parser.add_argument('--config', type=str, default=None, help='Path to a config file') # Ignores all other arguments if provided
parser.add_argument('--llm', action = 'store_true', help = 'Use a GPT 3.5 instance to generate prompts instead of static')

args = parser.parse_args()

def run_prompt_generator(args) : 
    '''
    Run the prompt generator
    args : arguments from the command line    
    '''
    if args.config is None : 
        prompts, objects = dinos_maker.make_prompts(args.seed, args.num_prompts, args.topic, args.num_per_prompt, args.constraint_type, args.llm)
    else : 
        with open(args.config, 'r') as f : 
            config = json.load(f)
        num_prompts = int(config.get('num_prompts'))
        seed = int(config.get('seed'))
        topic = config.get('topic')
        if topic == 'False' : 
            topic = False
        else :
            topic = True
        llm = config.get('llm')
        if llm == 'False' :
            llm = False
        else :
            llm = True
        num_per_prompt = int(config.get('num_per_prompt'))
        constraint_type = config.get('constraint_type')
        if constraint_type == 'None' : 
            constraint_type = []
        prompts, objects = dinos_maker.make_prompts(seed, num_prompts, topic, num_per_prompt, constraint_type, llm)
    # Save the prompts to a json file
    df = pd.DataFrame(prompts, columns = ['Prompt', "Constraint Type"])
    output = config.get('output', 'random_prompts.json') if args.config is not None else args.output
    df.to_json(output, default_handler=str)
    print("Prompts saved to", args.output)
    import pickle
    with open(output.replace('.json', '.pkl'), 'wb') as f:
        pickle.dump(objects, f)
    print("Objects saved to", output.replace('.json', '.pkl'))

if __name__ == '__main__':
    run_prompt_generator(args)
