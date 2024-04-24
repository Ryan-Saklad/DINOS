import json
import requests
import csv
import time
import os


def generate_response(messages: list, model: str, api_key: str) -> dict[str, dict] | None:
    """Generate a response using the OpenRouter service"""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            data = json.dumps({
                "model": model,
                "messages": messages
            })
        )
        result = response.json()
    except Exception as e:
        print(repr(e))
        return None

    if 'error' in response:
        print(response)
        return None

    return result


def generate_batch_responses(batch_prompts: list, model: str, api_key: str, prompt_limit: int = 3) -> list[list[str]] | None:
    responses = []
    for prompt in batch_prompts:
        messages = [{'role': 'user', 'content': prompt}]
        response = None
        prompt_count = 0
        while response is None and prompt_count < prompt_limit:
            response = generate_response(messages=messages, model=model, api_key=api_key)
            if response is None:
                print(f'Unable to generate response. Attempt {prompt_count+1}')
                time.sleep(0.5)
            prompt_count += 1

        if response is None:
            return None

        response = response['choices'][0]['message']['content']
        print(response)
        responses.append([response])

    return responses


def read_dinos_csv(file_path: str) -> list[str]:
    contents = list()
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            contents.append(row[0])

    if contents[0] not in ['Prompt', 'Response']:
        raise csv.Error('Unable to read file')

    return contents[1:]


def write_dinos_csv(file_path: str, contents: list[list[str]]) -> None:
    with open(file_path, 'a+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        for row in contents:
            csv_writer.writerow(row)


def read_dinos_json(file_path: str) -> dict[dict, dict]:
    with open(file_path) as jsonfile:
        contents = json.load(jsonfile)
        return contents


def get_model_name(openrouter_model_name: str) -> str:
    """Use to strip characters that cause issues with filenames and paths"""
    model_name = openrouter_model_name.split('/')[-1]
    model_name = model_name.split(':')[0]
    return model_name
