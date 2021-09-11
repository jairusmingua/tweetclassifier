# Tweet fire report classifier
## About this repo
This repo demonstrates the capability of classifying fire-related tweets using pre-trained BERT tagalog [models by jcblaise](https://huggingface.co/jcblaise) 

## File Structure
This repo consists of several directories
* static - contains audio files for notification system of the product and dataset for testing out the product
* templates - contains html template files for future web implementation of this product
* utils - contains tools to structure this codebase to be reusable
* finetuned_model - location of your trained bert classifier model

Sample file structure when the model is loaded
```
├── /finetuned_model
    ├── added_tokens.json
    ├── config.json
    ├── pytorch_model.bin
    ├── special_tokens_map.json
    ├── tokenizer_config.json
    ├── tokenizer.json
    └── vocab.txt
├── /static
├── /audio
├── /datasets
├── /templates
├── /utils
├── app.py
├── requirements.txt
├── test.py
├── tweetserver.py
├── README.md

```

## Usage
To run this application, you will be needing a finetuned bert tagalog model that detects fire-related tweets. This must be contained in the root directory with a folder named 'finedtuned-model'. [See File Structure](#file-structure)

There are two ways to run the application:
- Fetch tweets from TwitterAPI (twitter api bearer token required)
- Fetch tweets from a dataset

### Fetch Tweets from Twitter API
Assuming you have placed your model to the working directory, you must add bearer token from your twitter developer account. Create an **.env** file and set BEARER_TOKEN=[Twitter Bearer Token].

After this, you are now ready to run the application by executing:

```
    python app.py
```
### Fetch Tweets From a Dataset
If you want to create a sample stream with your datasets. You can create a tweet server for the application to fetch tweets via your local network. Don't forget to place the dataset (.csv format) to the [datsets](#file-structure) folder and rename the file as **dataset.csv**

To run a tweet server execute:
(Your tweets can be defaulty accessed on **http://localhost:5000**)
```
    python tweetserver.py
```
After running the tweetserver run the classifier application:
- Dont forget to add a --local flag to let application know where to fetch

```
    python app.py [--local] [--host HOST] [--port PORT] 
```
Example execution of application fetching on **localhost** in port **5000**
```
    python app.py --local --host localhost --port 5000
```

Resources:
* [jcblaisecruz02/Filipino-Text-Benchmarks](https://github.com/jcblaisecruz02/Filipino-Text-Benchmark)
