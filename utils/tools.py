import re
import time 
import torch
import emoji
import shutil
import os

def tokenize(tweets) -> str:
    tweets = re.sub("\B\@([\w\-]+)","[MENTION]",tweets)
    tweets = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "[LINK]", tweets)
    tweets = re.sub("\B\#([\w\-]+)", "[HASHTAG]",tweets)#Remove hashtag sign but keep the text
    tweets = " ".join(tweets.split())
    tweets = ''.join(c for c in tweets if c not in emoji.UNICODE_EMOJI)
    return tweets


def classify_text(model, tokenizer, text) -> dict:
    masked = tokenize(text)
    tokens = tokenizer([masked], padding='max_length', truncation='longest_first', max_length=128, return_tensors='pt')
    start = time.time()
    with torch.no_grad():
        out = model(**tokens)[0]
    pred = out.argmax(1).item() # Outputs "0" which means "may sunog"
    end = time.time()
    return pred, text, masked, end-start


def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')
   # print out some text


def print_centre(s):
  
    for _ in range(int(shutil.get_terminal_size().lines)//int(5)):
        print('\n')
    print(s.center(shutil.get_terminal_size().columns))