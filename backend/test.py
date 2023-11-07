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

"""
data_frames = []
directory_path = './'
for filename in os.listdir(directory_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory_path, filename)

        # Read the CSV and selected desired columns
        data = pd.read_csv(file_path)
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

            # Order the DataFrame based on 'engagement'
            data = data.sort_values(by='engagement', ascending=False)

            # Take the top 100 tweets
            top_100_tweets = data.head(20)

            data_frames.append(top_100_tweets)
        except Exception as E:
            print("ISSUE WITH THE FOLLOWING FILE:", filename)
            print(E)

big_data_frame = pd.concat(data_frames, ignore_index=True)
big_data_frame.drop_duplicates(subset='text', keep='first', inplace=True)
big_data_frame = big_data_frame.sample(frac=1).reset_index(drop=True)
output_csv_path = 'big_data.csv'
big_data_frame.to_csv(output_csv_path, index=False)
"""


files = [
         "RedTide_Pinellas.StPete_all_SIMPLE_columns.csv", "RedTide_Sarasota_all_SIMPLE_columns.csv"
         ]
file_path = 'RedTide_Sarasota_all_SIMPLE_columns.csv'

data = pd.read_csv(file_path, nrows=300)
Analysis().analyze_files(data)

geo = Util().non_geo_hashtags_dict
data = [{"text": key, "value": value} for key, value in geo.items()]

file_name = "non_geo_Sarasota.json"

# Open the file for writing and save the dictionary as JSON
with open(file_name, 'w') as json_file:
    json.dump(data, json_file)


