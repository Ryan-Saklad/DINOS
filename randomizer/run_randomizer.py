import argparse
import dinos_maker
import pandas as pd

parser = argparse.ArgumentParser(description='Generate random prompts for the Dinos Maker')
parser.add_argument('--num_prompts', type=int, default=1, help='Number of prompts to generate')
parser.add_argument('--topic', action='store_true', help='Include a topic in the prompt or let the model decide')
parser.add_argument('--seed', type=int, default=None, help='Seed for random number generator')
parser.add_argument('--output', type=str, default='random_prompts.csv', help='Output file path for the prompts')
args = parser.parse_args()

def run_prompt_generator(args) : 
    '''
    Run the prompt generator
    args : arguments from the command line    
    '''
    prompts = dinos_maker.make_prompts(args.seed, args.num_prompts, args.topic)
    # Save the prompts to a csv file
    df = pd.DataFrame(prompts, columns = ['Prompt'])
    df.to_csv(args.output , index = False)

run_prompt_generator(args)