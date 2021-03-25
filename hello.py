from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import argparse
import time
print("start")
start = time.time()
model = AutoModelForSequenceClassification.from_pretrained('finetuned_model')

parser = argparse.ArgumentParser(description="Text classifier")
parser.add_argument('tweet',help="Tweet")


tokenizer = AutoTokenizer.from_pretrained('finetuned_model')
# device = torch.device("cpu")
# model.to(device)
args = parser.parse_args()
text = args.tweet


tokens = tokenizer([text], padding='max_length', truncation='longest_first', max_length=128, return_tensors='pt')

with torch.no_grad():
    out = model(**tokens)[0]
pred = out.argmax(1).item() # Outputs "0" which means "may sunog"

print("May sunog" if pred==1 else "Walang sunog")

end = time.time()
print('Takes: '+str(end - start))