import os
from misc.utils import openrouter_utils
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']
TARGET_MODEL = 'mistralai/mistral-7b-instruct:nitro'
MODELS = [
    'mistralai/mistral-7b-instruct:nitro',
    'google/gemma-7b-it:nitro',
    'mistralai/mixtral-8x7b-instruct:nitro',
    'huggingfaceh4/zephyr-7b-beta',
]
prompts_csv = os.path.join('..', '..', 'randomizer', 'random_prompts.csv')
prompts = openrouter_utils.read_dinos_csv(prompts_csv)


def main():
    for i, prompt in enumerate(prompts):
        print(i, prompt)


if __name__ == '__main__':
    main()
