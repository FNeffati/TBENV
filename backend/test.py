import csv
import os
import pandas as pd
import re
from util import Util
from Analysis import Analysis
import json

"""
Read in files
Calculate engagement per tweet
Remove duplicates
Order the file based on engagement
Take the top 100 tweets
Add them
"""
"""total = 0
data_frames = []
directory_path = './'
for filename in os.listdir(directory_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory_path, filename)

        # Read the CSV and selected desired columns
        data = pd.read_csv(file_path)
        print("LENGTH OF CURRENT DATA FOR", filename,  len(data))

        total =+ len(data)
        labelled_accounts_df = pd.read_csv("finalized_8K_accounts_emojis_replaced.csv")
        labelled_accounts_df = labelled_accounts_df[["hand.label", "username"]]
        labelled_accounts_df.rename(columns={'hand.label': 'label'}, inplace=True)
        try:
            # calculating the 'engagement' metric
            engagement_columns = ['public_metrics.x_retweet_count', 'public_metrics.x_reply_count',
                                  'public_metrics.x_like_count', 'public_metrics.x_quote_count',
                                  'public_metrics.x_impression_count']
            data['engagement'] = data[engagement_columns].sum(axis=1)

            selected_columns = ['text', 'username', 'created_at.x', 'profile_image_url', 'location', 'engagement']
            data = data[selected_columns]
            data.rename(columns={'created_at.x': 'time', 'profile_image_url': 'image'}, inplace=True)
            # Extract date part from the 'time' column
            data['time'] = data['time'].str.split(' ').str[0]

            # Remove duplicates based on 'text' column
            data.drop_duplicates(subset='text', keep='first', inplace=True)

            # updating the location column with county name
            if 'Pasco' in filename:
                data['location'] = 'Pasco'
            elif 'Pinellas' in filename:
                data['location'] = 'Pinellas'
            elif 'Hillsborough' in filename:
                data['location'] = 'Hillsborough'
            elif 'Manatee' in filename:
                data['location'] = 'Manatee'
            elif 'Sarasota' in filename:
                data['location'] = 'Sarasota'
            
            # TODO: Add a account type column
            data = pd.merge(data, labelled_accounts_df, on='username', how='left')
            data.fillna('No Label', inplace=True)


            # Order the DataFrame based on 'engagement'
            data = data.sort_values(by='engagement', ascending=False)

            # Take the top 200 tweets
            top_100_tweets = data.head(100)

            data_frames.append(top_100_tweets)
        except Exception as E:
            print("ISSUE WITH THE FOLLOWING FILE:", filename)
            print(E)

big_data_frame = pd.concat(data_frames, ignore_index=True)
big_data_frame.drop_duplicates(subset='text', keep='first', inplace=True)
big_data_frame = big_data_frame.sample(frac=1).reset_index(drop=True)

import pymongo

MONGO_URI = "mongodb+srv://Neffati:y4m4SKKmoIg6riCP@cluster0.h1xa7vw.mongodb.net/?retryWrites=true&w=majority"
connection = pymongo.MongoClient(MONGO_URI)

db = connection.tweets
all_tweets = db.all_tweets

all_tweets.insert_many(big_data_frame.to_dict('records'))
"""

"""output_csv_path = 'big_data.csv'
big_data_frame.to_csv(output_csv_path, index=False)

"""
# print("TOTAL IS: ", total)
# TODO: Take the Tweets from the big file that correspond to the input county
#
"""
I have a csv file that has tweets and their corresponding county 
I want a function that based on the input county, selects and return the rows with the corresponding county


"""
"""
target_county = 'big_data'

data = pd.read_csv('big_data.csv')

# Filter the rows based on the target county
filtered_data = data[data['location'] == target_county]
print(len(filtered_data))
Analysis().analyze_files(data)

non_geo = Util().non_geo_hashtags_dict
non_geo_data = [{"text": key, "value": value} for key, value in non_geo.items()]

file_name = "non_geo_" + target_county + ".json"
with open(file_name, 'w') as json_file:
    json.dump(non_geo_data, json_file)"""

"""
geo = Util().geo_tag_dict
geo_data = [{"text": key, "value": value} for key, value in geo.items()]

file_name = "geo_" + target_county + ".json"
with open(file_name, 'w') as json_file:
    json.dump(geo_data, json_file)
"""

"""
import pymongo

MONGO_URI = "mongodb+srv://Neffati:y4m4SKKmoIg6riCP@cluster0.h1xa7vw.mongodb.net/?retryWrites=true&w=majority"
connection = pymongo.MongoClient(MONGO_URI)

db = connection.tags_frequency
non_geo_tags = db.geo_tags

type_of_cloud = "Geo Tags"
county = "Sarasota"

prefix = "non_geo_"
suffix = "big_data.json"

if type_of_cloud == "Non-Geo Tags":
    prefix = "non_geo_"
if type_of_cloud == "Geo Tags":
    prefix = "geo_"

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
with open(file, 'r') as json_file:
    terms = json.load(json_file)
    current_file = {county: terms}
    non_geo_tags.insert_one(current_file)"""



"""from datetime import datetime

import pymongo

MONGO_URI = "mongodb+srv://Neffati:y4m4SKKmoIg6riCP@cluster0.h1xa7vw.mongodb.net/?retryWrites=true&w=majority"
connection = pymongo.MongoClient(MONGO_URI)

db = connection.tweets
all_tweets = db.all_tweets


# Define the format of your date string (e.g., 'YYYY-MM-DD')
date_format = "%Y-%m-%d"  # Adjust this format to match your date strings

# Iterate over each document
for doc in all_tweets.find():
    # Convert the date string to a datetime object
    if 'time' in doc and isinstance(doc['time'], str):
        try:
            new_date = datetime.strptime(doc['time'], date_format)
            # Update the document with the new datetime object
            all_tweets.update_one({'_id': doc['_id']}, {'$set': {'time': new_date}})
        except ValueError as e:
            print(f"Error converting date for document {doc['_id']}: {e}")"""

