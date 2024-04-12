import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

MODEL = 'mistralai/mistral-7b-instruct:nitro'


def generate_response(messages: list, model: str) -> str | None:
    """Generate a response using the OpenRouter service"""
    OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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


def main():
    pass


if __name__ == '__main__':
    main()
