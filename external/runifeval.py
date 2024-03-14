import os, json, pprint, datetime, csv, subprocess
import requests

import pandas as pd

from dotenv import load_dotenv

load_dotenv()


# TODO refactor jsonl read and save operations
# make sure to update these paths if the relative path
# to instruction_following_eval/ changes
DATA_PATH = os.path.join('.', 'instruction_following_eval', 'data')
PROMPTS_PATH = os.path.join(
    DATA_PATH, 'input_response_data_gpt4_20231107_145030.jsonl')
NUM_PROMPTS = 541


def get_llm_response(messages: list, model: str) -> str:
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
        
    # TODO be more specific with potential exceptions
    except Exception as e:
        print(repr(e))
        return {'error': 'error'}
    
    print(f"Response keys: {result.keys()}")
    return result


# TODO convert to use input_data.jsonl
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
        prompt_count = 0
        while 'error' in response and prompt_count < 5:
            # keep requesting a response until the rate limit subsides
            response = get_llm_response(messages=messages, model=model)

            # to prevent getting stuck if there are many exceptions
            prompt_count += 1  
            # print(f"\tResponse: {response}")

        prompt_response = {
            "prompt": prompt,
            "response": response
        }
        prompt_response_list.append(prompt_response)
    
    return prompt_response_list


def save_ifeval_input_data(
        model: str, prompt_responses: list, model_datetime: str) -> str:
    # saved files are differentiated by model and date
    model_name = model.split('/')[-1]
    filename = '_'.join([
        'input_response_data',
        model_name,
        model_datetime]) + '.jsonl'
    save_filepath = os.path.join(DATA_PATH, filename)

    with open(save_filepath, mode='w', encoding='utf-8') as save_file:
        for prompt_response in prompt_responses:

            # reformat the responses to only include content
            message = prompt_response["response"]["choices"][0]["message"]
            prompt_response_obj = {
                "prompt": prompt_response["prompt"],
                "response": message["content"]
            }
            print(prompt_response_obj)
            
            save_file.write(json.dumps(prompt_response_obj) + "\n")
    
    return save_filepath


def get_instruction_ids() -> list:
    input_data_file = os.path.join(DATA_PATH, 'input_data.jsonl')

    instruction_ids = set()
    with open(input_data_file, mode='r', encoding='utf-8') as f:
        jlines = f.read().splitlines()
        jlines = [json.loads(jline) for jline in jlines]
        for jline in jlines:
            instruction_ids |= set(jline["instruction_id_list"])
    
    # print(instruction_ids)
    return sorted(instruction_ids)


def get_instruction_id_counts() -> dict:
    input_data_file = os.path.join(DATA_PATH, 'input_data.jsonl')
    instruction_id_cts = {}
    with open(input_data_file, mode='r', encoding='utf-8') as f:
        for jline in f:
            line = json.loads(jline)
            instruction_id_list = line['instruction_id_list']
            for instr_id in instruction_id_list:
                count = instruction_id_cts.setdefault(instr_id, 0)
                instruction_id_cts[instr_id] = count + 1
    
    return instruction_id_cts


def calculate_eval_percentages() -> None:
    df_results = pd.read_csv(os.path.join(DATA_PATH, 'eval_results.csv'),
                             encoding='utf-8')
    df_results_pct = df_results.copy()
    instr_id_cts = get_instruction_id_counts()
    df_results_pct['follow_all_instructions'] = \
        df_results['follow_all_instructions'] / NUM_PROMPTS
    for instr_id in instr_id_cts:
        df_results_pct[instr_id] = \
            df_results[instr_id] / instr_id_cts[instr_id]
    df_results_pct.to_csv(os.path.join(DATA_PATH, 'eval_results_pct.csv'))
    


def save_evaluation_results(model: str, model_datetime: str):
    loose_file = os.path.join(DATA_PATH, 'eval_results_loose.jsonl')
    strict_file = os.path.join(DATA_PATH, 'eval_results_strict.jsonl')
    eval_results_file = os.path.join(DATA_PATH, 'eval_results.csv')
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
                for instruction_id, result in zip(
                    line_instruction_ids, inst_results):
                    # print(instruction_id, result)
                    if result:
                        eval_dict[instruction_id] += 1

        # store the results for this model and accuracy in a csv file
        need_header = False if os.path.exists(eval_results_file) else True
        with open(eval_results_file, mode='a',
                  encoding='utf-8', newline='') as csvfile:
            eval_results_writer = csv.writer(csvfile)

            if need_header:
                header_row = ['model',
                              'datetime',
                              'accuracy',
                              'follow_all_instructions'] + all_instruction_ids
                eval_results_writer.writerow(header_row)

            # records the results
            results_row = [eval_dict["model"],
                           eval_dict["datetime"],
                           eval_dict["accuracy"],
                           eval_dict["follow_all_instructions"]]
            # record the results for each instruction id
            for instruction_id in all_instruction_ids:
                results_row.append(eval_dict[instruction_id])
            eval_results_writer.writerow(results_row)


def main():
    prompts = get_base_prompts()
    models = [
        # 'mistralai/mistral-7b-instruct:nitro',
        # 'google/gemma-7b-it:nitro',
        # 'mistralai/mixtral-8x7b-instruct:nitro',
        # 'huggingfaceh4/zephyr-7b-beta',
    ]

    for model in models:
        for runidx in range(3):
            print(f"{model} run {runidx + 1}")

            # separate runs are differentiated by model name and datetime
            model_datetime = datetime.datetime.today().strftime('%F_%T')

            # generate the responses to feed to the evaluation script
            input_response_data = get_ifeval_input_data(model, prompts)
            # TODO save in batches so you don't waste responses
            saved_file = save_ifeval_input_data(model, input_response_data, model_datetime)

            # run the evaluation script
            subprocess.run([
                "python", "-m", "instruction_following_eval.evaluation_main",
                "--input_data=./instruction_following_eval/data/input_data.jsonl",
                "--input_response_data=" + saved_file,
                "--output_dir=./instruction_following_eval/data/"
            ])

            # save the evaluation results for analysis
            save_evaluation_results(model, model_datetime)


if __name__ == '__main__':
    main()
