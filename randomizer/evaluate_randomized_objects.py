from benchmark import question
import pickle
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Evaluate the generated prompts')
parser.add_argument('--input', type=str, default='random_prompts.pkl', help='Input file path for the prompt pickled objects')
parser.add_argument('--output', type=str, default='evaluation_results.csv', help='Output file path for the evaluation results')
parser.add_argument('--model_response', type=str, default='model_responses.csv', help='Output file path for the model responses')
args = parser.parse_args()

def evaluate_prompts(args) :
    '''
    Evaluate the prompts
    args : arguments from the command line
    '''
    model_responses = list(pd.read_csv(args.model_response)['Response'])
    with open(args.input, 'rb') as f:
        prompt_objects = pickle.load(f)
    results = []
    for prompt in range(len(prompt_objects)) : 
        results.append(prompt_objects[prompt].evaluate_response(model_responses[prompt]))
    df = pd.DataFrame(results, columns = ['Correctness', 'Violated Constraints'])
    df.to_csv(args.output, index = False)
    print("Evaluation results saved to", args.output)

evaluate_prompts(args)