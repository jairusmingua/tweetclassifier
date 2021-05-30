from utils.stream import initialize_stream_header
import requests
import time
import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import threading
import pygame
import json
from utils.tools import (
    classify_text,
    tokenize,
    print_centre,
    screen_clear
)
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer
)
led = None
try:
    from gpiozero import LED
    led = LED(12)
except ImportError:
    print('GPIO Not Found')

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--local', action='store_true', help='Start in local mode given you have a tweet server')
parser.add_argument('--host', type=str, help='Hostname of the tweet server', default='localhost')
parser.add_argument('-p','--port', type=str, help='Port of the tweet server', default='5000')
args = parser.parse_args()
local = args.local
host = args.host
port = args.port

model = AutoModelForSequenceClassification.from_pretrained('finetuned_model')
tokenizer = AutoTokenizer.from_pretrained('finetuned_model')

def beep():
    pygame.mixer.init()
    pygame.mixer.music.load("./static/audio/notif.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


def alert():
    task = threading.Thread(target=beep)
    task.start()
    if led:
        for _ in range(3):
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5) 


def main():
    print(model)
    print('Model Loaded')
    if local:
        while True:
            screen_clear()
            r = requests.get(f'http://{host}:{port}').json()
            pred, text, masked, time_elapsed = classify_text(model,tokenizer,r.get('text'))
            print_centre(text)
            if pred == 1:
                task = threading.Thread(target=alert)
                task.start()
        
            time.sleep(10)

    else:
        headers = initialize_stream_header()
        with requests.get("https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,) as response:
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
                    pred, text, masked, time_elapsed = classify_text(model,tokenizer,json_response['data']['text'])
                    print_centre(text)

if __name__ == '__main__':
    main()