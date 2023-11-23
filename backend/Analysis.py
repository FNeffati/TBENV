import re
from datetime import datetime

from bson import json_util

from util import Util
import pandas as pd
import json
import pymongo


class Analysis:

    @staticmethod
    def preprocess_text_column(just_text_col):
        """
        :param just_text_col: Takes just the entire text column from the dataframe
        """
        tokenized_text_column = []
        for line in just_text_col:
            my_punct = ['!', '"', '$', '%', '&', "'", '(', ')', '*', '+', ',', '.',
                        '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '-',
                        '`', '{', '|', '}', '~', '»', '«', '“', '”']

            punct_pattern = re.compile("[" + re.escape("".join(my_punct)) + "]")
            line = re.sub(punct_pattern, "", line)
            line = re.sub(r"/[^\w\s\']|_/g, """, "", line)
            line = re.sub(r"/\s+/g, " "", "", line)
            line = re.sub(r"(https|www).*com", "", line)
            line = re.sub(r"\s+", " ", line)
            tokenized_text = line.split()

            if tokenized_text not in tokenized_text_column:
                hashtags = Util().extract_hashtags(tokenized_text)
                filtered_tags = Util().filter_hashtags(hashtags)
                Util().geo_tag_harvester(filtered_tags)
                tokenized_text_column.append(tokenized_text)

    def analyze_files(self, df):

        just_text_col = []
        for line in df["text"]:
            line = re.sub(r'\bhttps\w*\b.*', '', line)
            line = re.sub(r'\bhttp\w*\b.*', '', line)

            just_text_col.append(line)

        self.preprocess_text_column(just_text_col)

    def get_filtered_tweets(self, time_frame=None, county=None, account_type=None):
        """
        We want this function to filter based on requested params
        :param time_frame: this either goes in increments of 1 Day, week, month, year
                    or the user can give you a custom upper and lower bound
        :param county: a selected florida county that we will filter from
        :return: a dataframe with those rows
        """
        # TODO: Change this into a Database situation
        MONGO_URI = "mongodb+srv://Neffati:y4m4SKKmoIg6riCP@cluster0.h1xa7vw.mongodb.net/?retryWrites=true&w=majority"
        connection = pymongo.MongoClient(MONGO_URI)
        db = connection.tweets
        tweets = db.all_tweets
        query = {}

        if county or account_type or time_frame:
            if len(time_frame) == 2:
                start_date_str, end_date_str = time_frame

                # Convert strings to datetime objects
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

                print("Start Date:", start_date)
                print("End Date:", end_date)
                query = {
                    'time': {'$gte': start_date, '$lt': end_date}
                }
            if account_type:
                if account_type == "all":
                    query = {}
                else:
                    query["label"] = account_type
            if county:
                query["location"] = county
            cursor = tweets.find(query)
        else:
            cursor = tweets.find()

        results = []
        for doc in cursor:
            del doc["_id"]
            json_string = json.dumps(doc, default=json_util.default)
            results.append(json_string)

        print("------------------------------------------")
        print("LENGTH:", len(results))
        print("------------------------------------------")
        json_array = '[' + ', '.join(results) + ']'
        return json_array

    def get_key_words_frequency(self, type_of_cloud, county):
        MONGO_URI = "mongodb+srv://Neffati:y4m4SKKmoIg6riCP@cluster0.h1xa7vw.mongodb.net/?retryWrites=true&w=majority"
        connection = pymongo.MongoClient(MONGO_URI)
        db = connection.tags_frequency

        collection = db.non_geo_tags
        prefix = "non_geo_"
        suffix = "big_data.json"

        if type_of_cloud == "Non-Geo Tags":
            collection = db.non_geo_tags
            prefix = "non_geo_"
        if type_of_cloud == "Geo Tags":
            collection = db.geo_tags
            prefix = "geo_"
        if county == "All":
            terms = collection.find_one({county: {"$exists": True}})[county]
            return terms

        if county == "Pasco":
            suffix = "Pasco.json"
        if county == "Hillsborough":
            suffix = 'Hillsborough.json'
        if county == "Pinellas":
            suffix = 'Pinellas.json'
        if county == "Manatee":
            suffix = "Manatee.json"
        if county == "Sarasota":
            suffix = "Sarasota.json"

        file = prefix + suffix
        try:
            terms = collection.find_one({county: {"$exists": True}})[county]
            print("Pulled successfully from the database.")
        except Exception as e:
            with open(file, 'r') as json_file:
                print(e, "happened. So we're pulling from the files directly.")
                terms = json.load(json_file)
        return terms
