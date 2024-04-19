import json
import requests
import csv


def generate_response(messages: list, model: str, api_key: str) -> str | None:
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


def read_dinos_csv(file_path: str) -> list[str]:
    contents = list()
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            contents.append(row[0])

    return contents
