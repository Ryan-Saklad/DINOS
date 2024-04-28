def generate_instruct_instances(q_path, a_path) :
    import pandas as pd
    import json
    with open(q_path, 'r') as f:
        q = json.load(f)
    for i in q['Prompt'] : #Add question tag to each question
        q['Prompt'][i] = "Question: " + q['Prompt'][i]
    q_path = q_path.replace(".json", "_revised.json")
    json.dump(q, open(q_path, 'w'))
    print("Question file revised")
    df_answers = pd.read_csv(a_path)
    for i in range(len(df_answers['Response'])) :
        df_answers['Response'][i] = "Answer: " + df_answers['Response'][i]
    a_path = a_path.replace(".csv", "_revised.json")
    df_answers.to_json(a_path)
    print("Answer file revised")
    return True