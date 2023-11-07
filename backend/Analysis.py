import re
from util import Util
import pandas as pd
import json
from flask import g
from datetime import datetime, timedelta


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

    def get_filtered_tweets(self, time_frame=None, county=None):
        """
        We want this function to filter based on requested params
        :param time_frame: this either goes in increments of 1 Day, week, month, year
                    or the user can give you a custom upper and lower bound
        :param county: a selected florida county that we will filter from
        :return: a dataframe with those rows
        """
        # TODO: Change this into a Database situation
        file_path = 'big_data.csv'
        filtered_data = None
        try:
            data = pd.read_csv(file_path, nrows=300)

        except FileNotFoundError:
            print(FileNotFoundError, "There has been an issue with the following file:", file_path)
            data = None

        if data is not None:
            if county:
                filtered_data = data[data['location'] == county]
            else:
                filtered_data = data  # Return everything if no filters are provided
            """
            elif time_frame:

                # Calculate the upper bound (today's date)
                upper_bound = datetime.now().date()  # Use .date() to get only year, month, and day
                lower_bound = upper_bound - timedelta(days=365)

                # Calculate the lower bound based on the selected time frame
                if time_frame == '1 day':
                    lower_bound = upper_bound - timedelta(days=1)
                elif time_frame == '1 week':
                    lower_bound = upper_bound - timedelta(weeks=1)
                elif time_frame == '1 month':
                    lower_bound = upper_bound - timedelta(days=30)
                elif time_frame == '1 year':
                    lower_bound = upper_bound - timedelta(days=365)
                else:
                    # Handle invalid time_frame values here if needed
                    print("Invalid time frame selected")

                # Convert the 'time' column to a datetime object with only year, month, and day
                data['time'] = pd.to_datetime(data['time']).dt.date
                filtered_data = data[(data['time'] >= lower_bound) & (data['time'] <= upper_bound)]"""

        return filtered_data

    # TODO: Need to map certain locations to certain Counties in the drop box
    # TODO: Need to remove the extra: Florida or FL from the location column
    def get_key_words_frequency(self, type_of_cloud, county):

        prefix = "non_geo_"
        suffix = "big_set.json"

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
        return terms

