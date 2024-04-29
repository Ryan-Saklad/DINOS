import json
def gather_to_same_format(prompts, responses) :
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