# Tweet fire report classifier
## About this repo
This repo demonstrates the capability of classifying fire-related tweets using pre-trained BERT tagalog [models by jcblaise](https://huggingface.co/jcblaise) 

## File Structure
This repo consists of several directories
* static - contains audio files for notification system of the product and dataset for testing out the product
* templates - contains html template files for future web implementation of this product
* utils - contains tools to structure this codebase to be reusable

## Usage
To run this application, you will be needing a finetuned bert tagalog model that detects fire-related tweets. This must be contained in the root directory with a folder named 'finedtuned-model'.

You will be also be needing to run a tweet server 
```
    python tweetserver.py
```

After downloading and loading the model, run the following 
```
    python app.py [--local] [--host HOST] [--port PORT] 
```

If you have a twitter API bearer key, you can also run a live stream directly from twitter by running not running in local mode. 
```
    python app.py
```
Resources:
* [jcblaisecruz02/Filipino-Text-Benchmarks](https://github.com/jcblaisecruz02/Filipino-Text-Benchmark)
