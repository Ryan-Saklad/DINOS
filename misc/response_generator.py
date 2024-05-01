import os
import sys
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
    # 'mistralai/mixtral-8x7b-instruct:nitro',
    'mistralai/mistral-7b-instruct:nitro',
    'meta-llama/llama-2-70b-chat:nitro',
    'meta-llama/llama-3-8b-instruct:nitro',
    'meta-llama/llama-3-70b-instruct:nitro'
]
EVALUATION_DIR = os.path.join('evaluations', 'evaluation-20240426', 'test')
CURR_DATE = datetime.today().strftime('%F')
BATCH_SIZE = 5  # used to make intermittent writes to .csv file


def generate(prompts_json: str):
    # retrieve prompts
    contents = openrouter_utils.read_dinos_json(prompts_json)
    prompts = contents['Prompt']
    num_prompts = len(prompts)

    # calculate number of steps based on batch size
    steps = openrouter_utils.calculate_num_steps(num_prompts, BATCH_SIZE)

    for target_model in MODELS:
        print(f'Generating responses from {target_model}...')

        # prepare file path/names for output
        model_name = openrouter_utils.get_model_name(target_model)
        res_filename = f'responses_{model_name}_{CURR_DATE}_{num_prompts}.csv'
        res_path = os.path.join(EVALUATION_DIR, str(num_prompts), 'responses')
        res_csv = os.path.join(res_path, res_filename)
        miss_filename = f'missing_{model_name}_{CURR_DATE}_{num_prompts}.csv'
        miss_csv = os.path.join(EVALUATION_DIR, miss_filename)

        missing = [[res_filename]]
        for i in range(steps):
            start_idx = i * BATCH_SIZE
            end_idx = start_idx + BATCH_SIZE
            curr_batch = [prompts[str(i)] for i in range(start_idx, end_idx)]

            responses = openrouter_utils.generate_batch_responses(
                curr_batch, target_model, OPENROUTER_API_KEY,
                prompt_limit=3, temperature=0.0)

            # save indices for missing responses
            if responses is None:
                print(f'Unable to generate responses for prompts {start_idx} to {end_idx}.')
                responses = [['']] * BATCH_SIZE
                missing.append([start_idx, end_idx])  # the end_idx is not inclusive

            # header row for response file
            if i == 0:
                responses.insert(0, ['Response'])

            # save responses for the batch
            openrouter_utils.write_dinos_csv(res_csv, responses)

        if len(missing) > 1:
            print(f'Unable to generate responses for: {missing!r}')
            openrouter_utils.write_dinos_csv(miss_csv, missing)


if __name__ == '__main__':
    prompts_json = sys.argv[1]
    print(f'Generating responses to prompts at {prompts_json}')
    generate(prompts_json)
