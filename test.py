import time 
import math 
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer
)
import pandas as pd
from pandas.core.frame import DataFrame
from utils.tools import classify_text

def main():
    tweets: DataFrame = pd.read_csv('./static/datasets/eval_balanced_only.csv', delimiter = ",")
    model = AutoModelForSequenceClassification.from_pretrained('finetuned_model')
    tokenizer = AutoTokenizer.from_pretrained('finetuned_model')
    fp = 0
    tp = 0
    fn = 0
    tn = 0
    count = len(tweets.index-1) 
    print('Evaluation Starting....')
    start = time.time()
    for i in range(len(tweets.index-1)):
        text = tweets.loc[i]['text']
        label = int(tweets.loc[i]['label'])
        result = classify_text(model, tokenizer, text)
        if result['pred'] == label and label == 1:
            tp+=1
        if result['pred'] == label and label == 0:
            tn+=1
        if result['pred'] != label and label == 1:
            fp+=1
        if result['pred'] != label and label == 0:
            fn+=1

    end = time.time()
    mcc = ((tp*tn)-(fp*fn))/math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    print(f'True Positive: {tp}')
    print(f'False Positive: {fp}')
    print(f'True Negative: {tn}')
    print(f'False Negative: {fn}')
    print(f'N = {count}')
    print(f'MCC = {mcc}')
    print(f'Time Elapsed: {end-start}')
    
if __name__ == "__main__":
    main()