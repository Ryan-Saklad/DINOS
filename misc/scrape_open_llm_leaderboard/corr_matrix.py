from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

def main():
    json_data = []
    with open("open-llm-leaderboard.json", "r") as json_file:
        json_data = json.load(json_file)

    sns.set_theme(style="white")
    rs = np.random.RandomState(33)
    d = pd.DataFrame(data=rs.normal(size=(100, 26)), columns=list(ascii_letters[26:]))
    
    data = json_data
    df = pd.DataFrame(data)
    benchmarks = ["ARC", "HellaSwag", "MMLU", "TruthfulQA", "Winogrande", "GSM8K"]
    correlation_data = df[benchmarks]
    corr_matrix = correlation_data.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True)
    plt.title('Correlation Matrix of LLMs Performance on Benchmarks')
    plt.savefig('llm_corr_matrix.png')
    plt.show()
    

main()