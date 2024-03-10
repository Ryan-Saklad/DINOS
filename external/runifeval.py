import os, json, pprint, datetime, csv
import requests

from dotenv import load_dotenv

load_dotenv()


PROMPTS_PATH = os.path.join(
    '.', 'instruction_following_eval', 'data', 'input_response_data_gpt4_20231107_145030.jsonl')


def get_llm_response(messages: list, model: str) -> str:
    OPENROUTER_API_KEY = os.environ['OPENROUTER_API_KEY']

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
    print(f"Response keys: {result.keys()}")
    return result


def get_base_prompts(file: str=PROMPTS_PATH) -> list:
    with open(file, mode='r', encoding='utf-8') as jsonl:
        prompts = jsonl.read().splitlines()
        # print(prompts)

        return_list = []
        for jline in prompts:
            return_dict = json.loads(jline)
            del return_dict['response']
            return_list.append(return_dict)

        return return_list
    

def get_ifeval_input_data(model: str, prompts: list) -> list:
    # get llm responses to every prompt
    prompt_response_list = []
    for i, prompt in enumerate(prompts):
        prompt = prompt['prompt']
        print(f"{i+1}. Prompt: {prompt}")
        
        messages = [{"role": "user", "content": prompt}]
        # print(messages)

        response = {'error': 'error'}
        while 'error' in response:
            # keep requesting a response until the rate limit subsides
            response = get_llm_response(messages=messages, model=model)
            # print(f"\tResponse: {response}")

        prompt_response = {
            "prompt": prompt,
            "response": response
        }
        prompt_response_list.append(prompt_response)
    
    return prompt_response_list


def save_ifeval_input_data(model: str, prompt_responses: list, model_datetime: str) -> str:
    # saved files are differentiated by model and date
    model_name = model.split('/')[-1]
    filename = '_'.join([
        'input_response_data',
        model_name,
        model_datetime]) + '.jsonl'
    save_filepath = os.path.join(
        '.', 'instruction_following_eval', 'data', filename)

    with open(save_filepath, mode='w', encoding='utf-8') as save_file:
        for prompt_response in prompt_responses:

            # reformat the responses to only include content
            message = prompt_response["response"]["choices"][0]["message"]
            prompt_response_obj = {
                "prompt": prompt_response["prompt"],
                "response": message["content"]
            }
            print(prompt_response_obj)
            
            save_file.write(json.dumps(prompt_response) + "\n")
    
    return save_filepath


def get_instruction_ids() -> list:
    input_data_file = os.path.join('.', 'instruction_following_eval', 'data', 'input_data.jsonl')

    instruction_ids = set()
    with open(input_data_file, mode='r', encoding='utf-8') as f:
        jlines = f.read().splitlines()
        jlines = [json.loads(jline) for jline in jlines]
        for jline in jlines:
            instruction_ids |= set(jline["instruction_id_list"])
    
    # print(instruction_ids)
    return sorted(instruction_ids)


def save_evaluation_results(model: str, model_datetime: str):
    data_path = os.path.join('.', 'instruction_following_eval', 'data')
    loose_file = os.path.join(data_path, 'eval_results_loose.jsonl')
    strict_file = os.path.join(data_path, 'eval_results_strict.jsonl')
    eval_results_file = os.path.join(data_path, 'eval_results.csv')
    all_instruction_ids = get_instruction_ids()

    # pull all true from evaluation categories
    for file, accuracy in [[loose_file, 'loose'], [strict_file, 'strict']]:
        # store the number of correct responses
        eval_dict = dict(model=model, datetime=model_datetime,
                         accuracy=accuracy, follow_all_instructions=0)
        for instruction_id in all_instruction_ids:
            eval_dict[instruction_id] = 0

        # read the results
        with open(file, mode='r', encoding='utf-8') as fin:
            jlines = fin.read().splitlines()
            jlines = [json.loads(jline) for jline in jlines]
            for jline in jlines:
                # record results at the prompt level
                if jline["follow_all_instructions"]:
                    eval_dict['follow_all_instructions'] += 1
                
                # record results at the instruction level
                inst_results = jline["follow_instruction_list"]
                line_instruction_ids = jline["instruction_id_list"]
                for instruction_id, result in zip(line_instruction_ids, inst_results):
                    # print(instruction_id, result)
                    if result:
                        eval_dict[instruction_id] += 1

        # store the results for this model and accuracy in a csv file
        need_header = False if os.path.exists(eval_results_file) else True
        with open(eval_results_file, mode='a', encoding='utf-8', newline='') as csvfile:
            eval_results_writer = csv.writer(csvfile)

            if need_header:
                header_row = ['model', 'datetime', 'accuracy', 'follow_all_instructions'] + all_instruction_ids
                eval_results_writer.writerow(header_row)

            # records the results
            results_row = [eval_dict["model"], eval_dict["datetime"],
                           eval_dict["accuracy"], eval_dict["follow_all_instructions"]]
            # record the results for each instruction id
            for instruction_id in all_instruction_ids:
                results_row.append(eval_dict[instruction_id])
            eval_results_writer.writerow(results_row)


def main():
    prompts = get_base_prompts()
    models = [
        'mistralai/mistral-7b-instruct:nitro',
    ]

    for model in models:
        model_datetime = datetime.datetime.today().strftime('%F_%T')

        # input_response_data = get_ifeval_input_data(model, prompts)
        # saved_file = save_ifeval_input_data(model, input_response_data, model_datetime)
        save_evaluation_results(model, model_datetime)


if __name__ == '__main__':
    main()