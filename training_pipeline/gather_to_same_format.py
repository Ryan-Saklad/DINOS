import json
import pandas as pd
def gather_to_same_format(prompts, responses, evaluation = None) :
    if evaluation is None:
        with open(prompts) as f:
            prompts_json = json.load(f)
        with open(responses) as f:
            responses_json = json.load(f)
        prompts_json['Reponse'] = responses_json['Response']
        #Write the gathered data to a file
        prompts = prompts.replace('.json', "_same_format.json")
        with open(prompts, 'w') as f:
            json.dump(prompts_json, f)
            print("Wrote gathered data to same_format_training.json")
    else :
        with open(prompts) as f:
            prompts_json = json.load(f)
        with open(responses) as f:
            responses_json = json.load(f)
        eval_data = pd.read_csv(evaluation)
        prompts_answers_validate = {"Prompt" : {}, "Response" : {}}
        eval_data_list = list(eval_data["Partial Correctness"])
        for i in range(len(eval_data_list)):
            try :
                if "Partial Correctness Score = 1.0" in eval_data_list[i]:
                    prompts_answers_validate["Prompt"][i] = prompts_json["Prompt"][i]
                    prompts_answers_validate["Response"][i] = responses_json["Response"][i]
            except :
                continue
        #Write the gathered data to a file
        prompts = prompts.replace('.json', "_same_format_positive.json")
        with open(prompts, 'w') as f:
            json.dump(prompts_answers_validate, f)
            print("Wrote gathered data to same_format_training.json")