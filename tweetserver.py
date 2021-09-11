from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
from pandas.core.frame import DataFrame
app = Flask(__name__)
api = Api(app)
counter = -1
tweet: DataFrame = pd.read_csv('static/datasets/dataset.csv')

class Tweet(Resource):
    def get(self):
        global counter
        counter= counter+1 if counter<len(tweet.index) else 0

        return {'text':tweet.loc[counter]['text']}

api.add_resource(Tweet, '/')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

