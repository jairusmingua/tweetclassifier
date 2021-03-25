from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import argparse
import time
import flask
import requests
import logging
from stream import *
import re
import emoji
from threading import Thread,Lock
from flask import request,render_template
from flask_socketio import SocketIO,emit
from os import path,rename,remove
import shutil
import wget

from zipfile import ZipFile
#model prep
#check if model exists
model = None
tokenizer = None
done_downloading = False
parser = argparse.ArgumentParser()
parser.add_argument('--m',type=str,required=False,default='bert-tagalog-distilbert-tagalog-base-cased')
args = parser.parse_args()
model_name = str(args.m)
thread = None
thread_lock = Lock()
print('Default Model: '+model_name)

if(done_downloading==False):
    if(not path.exists(model_name+'/'+'finetuned_model')):
        print('Downloading Model...')
        wget.download('https://storage.googleapis.com/crested-drive-172104.appspot.com/'+model_name+'.zip')
        print('\nUnzipping Model')
        with ZipFile(model_name+'.zip', 'r') as zip_ref:
            zip_ref.extractall()
        remove(model_name+'.zip')
    model = AutoModelForSequenceClassification.from_pretrained(model_name+'/'+'finetuned_model')
    tokenizer = AutoTokenizer.from_pretrained(model_name+'/'+'finetuned_model')
    done_downloading = True

#flask socket prep
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
async_mode = None
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config["DEBUG"] = True
socketio = SocketIO(app,async_mode=async_mode)
#stream prep 


@app.route('/live',methods=['GET'])
def live():
    return render_template('live.html')
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/classify', methods=['GET'])
def classify():
    text = request.args.get("text")
    tokens = tokenizer([text], padding='max_length', truncation='longest_first', max_length=128, return_tensors='pt')
    start = time.time()
    with torch.no_grad():
        out = model(**tokens)[0]
    pred = out.argmax(1).item() # Outputs "0" which means "may sunog"
    end = time.time()
    print('Takes: '+str(end - start))
    return {'prediction':pred}
@socketio.event
def connect():
    print('connect')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=get_stream)
@socketio.on('hello')
def handle_hello(data):
    print('received message: ' + data['data'])
    socketio.emit('message','hello')

def get_stream():
    #connected using DummyJairusM
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAApVNAEAAAAAOjwvxNy1DK2YaYZAxUFVEHFVwvs%3DdTjiYcNJRrGmDZbToNOrI6a7bt5gI7nG9jpX9eXacPnpb1EOH5'
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    with requests.get("https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,) as response:
        print(response.status_code)
        sys.stdout.flush()
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                print(json_response['data']['text'])
                pred,text,masked= classify_text(json_response['data']['text'])
                socketio.emit("tweet",{'prediction':pred,'text':text,'masked':masked})
def classify_text(text):
    masked = tokenize(text)
    tokens = tokenizer([masked], padding='max_length', truncation='longest_first', max_length=128, return_tensors='pt')
    start = time.time()
    with torch.no_grad():
        out = model(**tokens)[0]
    pred = out.argmax(1).item() # Outputs "0" which means "may sunog"
    end = time.time()
    return pred,text,masked

def tokenize(tweets):
    tweets = re.sub("\B\@([\w\-]+)","[MENTION]",tweets)
    tweets = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "[LINK]", tweets)
    tweets = re.sub("\B\#([\w\-]+)", "[HASHTAG]",tweets)#Remove hashtag sign but keep the text
    tweets = " ".join(tweets.split())
    tweets = ''.join(c for c in tweets if c not in emoji.UNICODE_EMOJI)
    return tweets

if __name__ == '__main__':
    if(done_downloading):
        socketio.run(app=app,port=5000)




 





