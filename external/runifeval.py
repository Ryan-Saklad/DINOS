import os
import json
import pprint
import datetime
import csv
import subprocess
import time
import pandas as pd
from misc.utils.openrouter_utils import generate_response
from dotenv import load_dotenv

load_dotenv()


# update these paths if the relative path instruction_following_eval/ changes
DATA_PATH = os.path.join('.', 'instruction_following_eval', 'data')
PROMPTS_PATH = os.path.join(DATA_PATH, 'input_data.jsonl')
NUM_PROMPTS = 541


def read_jsonl(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        jsonl = f.read().splitlines()
        jlines = [json.loads(jline) for jline in jsonl]
        return jlines


def get_input_data(file: str = PROMPTS_PATH) -> list:
    """returns input data in batches"""
    input_data = read_jsonl(file)
    return input_data
    

def generate_responses(model: str, input_data: list) -> tuple[list, set]:
    """Generate a response to each prompt in the IfEval benchmark.
    Return a set of keys for any prompts that didn't get a valid response"""
    responses = []
    missing = set()
    for line in input_data:
        prompt = line['prompt']
        print(f"Prompt key: {line['key']}")
        
        messages = [{"role": "user", "content": prompt}]
        response = None
        prompt_count = 0
        while response is None and prompt_count < 3:
            response = generate_response(messages=messages, model=model, api_key=os.environ['OPENROUTER_API_KEY'])
            if response is None:
                time.sleep(1)  # the primary source of errors is rate limiting
            prompt_count += 1

        # if we aren't able to generate a valid response, return its key
        if response is None:
            missing.add(line['key'])
            continue

        responses.append(dict(prompt=prompt, response=response))

    return responses, missing


def save_ifeval_input_data(save_filepath: str,
                           prompt_responses: list,) -> None:

    with open(save_filepath, mode='a', encoding='utf-8') as save_file:
        for prompt_response in prompt_responses:

            try:
                # reformat the responses to only include content
                message = prompt_response["response"]["choices"][0]["message"]
                prompt_response_obj = {
                    "prompt": prompt_response["prompt"],
                    "response": message["content"]
                }
            # skip responses that don't have the expected data
            except KeyError as e:
                print(repr(e))
                pprint.pprint(prompt_response)
                continue
            
            save_file.write(json.dumps(prompt_response_obj) + "\n")


def get_instruction_ids(input_data: list) -> list:
    instruction_ids = set()
    for line in input_data:
        instruction_ids |= set(line['instruction_id_list'])

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
    df_results_pct.to_csv(os.path.join(DATA_PATH, 'eval_results_pct.csv'),
                          index=False)


def aggregate_results() -> None:
    df_results_pct = pd.read_csv(os.path.join(DATA_PATH, 'eval_results_pct.csv'))
    return df_results_pct


# def aggregate_instr_results() -> None:
#     df_results = pd.read_csv(os.path.join(DATA_PATH, 'eval_results.csv'))
#     instr_ids = get_instruction_ids()
#     agg_instr_ids = { instr_id.split(':')[0] for instr_id in instr_ids }
#     df_agg = pd.DataFrame()
#     for i, row in df_results.iterrows():
#         df_agg.loc[i, 'model'] = row['model']
#         df_agg.loc[i, 'datetime'] = row['datetime']
#         df_agg.loc[i, 'accuracy'] = row['accuracy']
#         df_agg.loc[i, 'follow_all_instructions'] = row['follow_all_instructions']
#         cols = list(row.axes)
#         for instr in cols:
#             agg_instr = instr.split(':')[0]
#             if instr in agg_instr_ids:
#                 if agg_instr in df_agg.columns:
#                     df_agg.loc[i, agg_instr] += row[instr]


def save_evaluation_results(model: str, model_datetime: str,
                            input_data: list):
    loose_file = os.path.join(DATA_PATH, 'eval_results_loose.jsonl')
    strict_file = os.path.join(DATA_PATH, 'eval_results_strict.jsonl')
    eval_results_file = os.path.join(DATA_PATH, 'eval_results.csv')
    all_instruction_ids = get_instruction_ids(input_data)

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


def build_save_filepath(model: str, model_datetime: str, runIdx: int) -> str:
    model_name = model.split('/')[-1]
    filename = '_'.join(['input_response_data', model_name,
                         model_datetime, str(runIdx)]) + '.jsonl'
    return os.path.join(DATA_PATH, filename)


def main():
    input_data = get_input_data(PROMPTS_PATH)
    missing = {line['key'] for line in input_data}

    models = [
        # 'mistralai/mistral-7b-instruct:nitro',
        # 'google/gemma-7b-it:nitro',
        # 'mistralai/mixtral-8x7b-instruct:nitro',
        # 'huggingfaceh4/zephyr-7b-beta',
        'perplexity/sonar-small-chat',
        'perplexity/sonar-small-online'
    ]

    for model in models:
        for runIdx in range(3):
            print(f"{model} run {runIdx + 1}")

            # differentiate runs by model name and datetime
            model_datetime = datetime.datetime.today().strftime('%F')
            save_filepath = build_save_filepath(model, model_datetime, runIdx)

            # generate the responses to feed to the evaluation script
            model_run_count = 0
            while len(missing) and model_run_count < 3:
                # keep generating responses for prompts that didn't get a valid response
                input_data = [line for line in input_data if line['key'] in missing]
                input_response_data, missing = generate_responses(model, input_data)
                save_ifeval_input_data(save_filepath, input_response_data)

            # run the evaluation script
            subprocess.run([
                "python", "-m", "instruction_following_eval.evaluation_main",
                "--input_data=./instruction_following_eval/data/input_data.jsonl",
                "--input_response_data=" + save_filepath,
                "--output_dir=./instruction_following_eval/data/"
            ])

            # save the evaluation results for analysis
            save_evaluation_results(model, model_datetime, input_data)


if __name__ == '__main__':
    main()
