import os
from datetime import datetime
from misc.utils import openrouter_utils
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']
MODELS = [
    'openai/gpt-4-turbo',
    'openai/gpt-3.5-turbo',
    'anthropic/claude-3-opus',
    'anthropic/claude-3-haiku',
    'mistralai/mixtral-8x7b-instruct:nitro',
    'mistralai/mistral-7b-instruct:nitro',
    'meta-llama/llama-2-70b-chat:nitro',
    'meta-llama/llama-3-8b-instruct:nitro',
    'meta-llama/llama-3-70b-instruct:nitro'
]
EVALUATION_DIR = os.path.join('evaluations', 'evaluation-20240426')
target_model = MODELS[8]
model_name = openrouter_utils.get_model_name(target_model)
prompts_json = os.path.join(EVALUATION_DIR, 'random_prompts_3.json')
curr_date = datetime.today().strftime('%F')
responses_file_name = 'model_responses_' + model_name + '_' + curr_date + '_3' + '.csv'
responses_csv = os.path.join(EVALUATION_DIR, responses_file_name)
missing_file_name = 'missing_' + model_name + '_' + curr_date + '.log'
missing_log = os.path.join(EVALUATION_DIR, missing_file_name)
BATCH_SIZE = 5


def main():
    contents = openrouter_utils.read_dinos_json(prompts_json)
    prompts = contents['Prompt']
    constraints = contents['Constraint Type']

    steps = len(prompts) // BATCH_SIZE
    steps += 1 if len(prompts) % BATCH_SIZE > 0 else 0

    missing = []
    for i in range(steps):
        start_idx = i * BATCH_SIZE
        end_idx = start_idx + BATCH_SIZE
        curr_batch = [prompts[str(i)] for i in range(start_idx, end_idx)]

        responses = openrouter_utils.generate_batch_responses(curr_batch,
                                                              target_model,
                                                              OPENROUTER_API_KEY,
                                                              prompt_limit=3,
                                                              temperature=0.0)

        if responses is None:
            print(f'Unable to generate responses for prompts {start_idx} to {end_idx}.')
            responses = [['']] * BATCH_SIZE

            # the end_idx is not inclusive
            missing.append([start_idx, end_idx])
        if i == 0:
            responses.insert(0, ['Response'])

        openrouter_utils.write_dinos_csv(responses_csv, responses)

    if len(missing):
        print(f'Unable to generate responses for: {missing!r}')


if __name__ == '__main__':
    main()
