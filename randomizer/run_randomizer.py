import argparse
from randomizer import dinos_maker
import pandas as pd
import json

parser = argparse.ArgumentParser(description='Generate random prompts for the Dinos Maker')
parser.add_argument('--num_prompts', type=int, default=1, help='Number of prompts to generate')
parser.add_argument('--topic', action='store_true', help='Include a topic in the prompt or let the model decide')
parser.add_argument('--seed', type=int, default=None, help='Seed for random number generator')
parser.add_argument('--output', type=str, default='random_prompts.csv', help='Output file path for the prompts')
parser.add_argument('--num_per_prompt', type=int, default=-1, help='Number of constraints per prompt, defaults to no limit')
parser.add_argument('--constraint_type', type=str, default=None, help='Type of constraint to generate, defaults to random')
parser.add_argument('--config', type=str, default=None, help='Path to a config file') # Ignores all other arguments if provided

args = parser.parse_args()

def run_prompt_generator(args) : 
    '''
    Run the prompt generator
    args : arguments from the command line    
    '''
    if args.config is None : 
        prompts, objects = dinos_maker.make_prompts(args.seed, args.num_prompts, args.topic, args.num_per_prompt, args.constraint_type)
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
        num_per_prompt = int(config.get('num_per_prompt'))
        constraint_type = config.get('constraint_type')
        if constraint_type == 'None' : 
            constraint_type = None
        output = config.get('output', 'random_prompts.csv')
        prompts, objects = dinos_maker.make_prompts(seed, num_prompts, topic, num_per_prompt, constraint_type)
    # Save the prompts to a csv file
    df = pd.DataFrame(prompts, columns = ['Prompt', ["Constraint Type"]])
    df.to_csv(args.output , index = False)
    print("Prompts saved to", args.output)
    import pickle
    with open(args.output.replace('.csv', '.pkl'), 'wb') as f:
        pickle.dump(objects, f)
    print("Objects saved to", args.output.replace('.csv', '.pkl'))

if __name__ == '__main__':
    run_prompt_generator(args)
