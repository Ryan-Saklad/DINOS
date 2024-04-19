import os
from datetime import datetime
from misc.utils import openrouter_utils
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']
MODELS = [
    'mistralai/mistral-7b-instruct:nitro',
    'google/gemma-7b-it:nitro',
    'mistralai/mixtral-8x7b-instruct:nitro',
    'huggingfaceh4/zephyr-7b-beta',
]
target_model = MODELS[0]
model_name = openrouter_utils.get_model_name(target_model)
prompts_csv = os.path.join('..', '..', 'randomizer', 'random_prompts.csv')
responses_file_name = 'model_responses_' + model_name + '_' + datetime.today().strftime('%F') + '.csv'
responses_csv = os.path.join('..', '..', 'randomizer', responses_file_name)
BATCH_SIZE = 5


def main():
    prompts = openrouter_utils.read_dinos_csv(prompts_csv)

    steps = len(prompts) // BATCH_SIZE
    steps += 1 if len(prompts) % BATCH_SIZE > 0 else 0

    missing = []
    for i in range(steps):
        start_idx = i * BATCH_SIZE
        end_idx = start_idx + BATCH_SIZE
        curr_batch = prompts[start_idx:end_idx]

        responses = openrouter_utils.generate_batch_responses(
            curr_batch, target_model, OPENROUTER_API_KEY, prompt_limit=3
        )

        if responses is None:
            print(f'Unable to generate responses for prompts {start_idx} to {end_idx}.')
            responses = [['']] * BATCH_SIZE
            missing.append([start_idx, end_idx])
        if i == 0:
            responses.insert(0, ['Response'])

        openrouter_utils.write_dinos_csv(responses_csv, responses)

    print(f'Unable to generate responses for: {missing!r}')


if __name__ == '__main__':
    main()
