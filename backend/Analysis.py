import re
from util import Util
from SentimentAnalysis import *


class Analysis:

    @staticmethod
    def preprocess_text_column(just_text_col):
        """
        :param just_text_col: Takes just the text column from the dataframe
        :return: a tokenized and partially cleaned text column
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
            # tokenized_text = word_tokenize(line)
            if tokenized_text not in tokenized_text_column:
                # I should remove our own stop words here:
                hashtags = Util().extract_hashtags(tokenized_text)
                filtered_tags = Util().filter_hashtags(hashtags)
                Util().geo_tag_harvester(filtered_tags)
                tokenized_text_column.append(tokenized_text)
        return tokenized_text_column

    def analyze_files(self, file):
        """
        Takes in a list of file urls, downloads each file, and generates uni-gram, bi-gram, and tri-gram frequency dictionaries for
        their text column. Returns a dictionary of n-gram frequency dictionaries for each file.
        """


        just_text_col = []
        for line in df["text"]:
            line = re.sub(r'\bhttps\w*\b.*', '', line)
            just_text_col.append(line)

        self.preprocess_text_column(just_text_col)


if __name__ == '__main__':
    analysis_hub = Analysis()
    list_of_files = [
        "https://raw.githubusercontent.com/UsDAnDreS/EnvironmentalTwitter/main/Data/RedTide_Pasco_all_SIMPLE_columns"
        ".csv",
        "https://raw.githubusercontent.com/UsDAnDreS/EnvironmentalTwitter/main/Data/RedTide_Tampa_all_SIMPLE_columns"
        ".csv",
        "https://raw.githubusercontent.com/UsDAnDreS/EnvironmentalTwitter/main/Data"
        "/RedTide_Sarasota_all_SIMPLE_columns.csv",
        "https://raw.githubusercontent.com/UsDAnDreS/EnvironmentalTwitter/main/Data/RedTide_Pinellas"
        ".StPete_all_SIMPLE_columns.csv",
        "https://raw.githubusercontent.com/UsDAnDreS/EnvironmentalTwitter/main/Data"
        "/RedTide_Manatee_all_SIMPLE_columns.csv "
    ]

    for file in list_of_files:
        analysis_hub.analyze_files(file)

        geo_tag_dict = Util().geo_tag_dict
        popular_hashtags_dict = Util().non_geo_hashtags_dict

        top_n_geo_hashtags = sorted(geo_tag_dict, key=geo_tag_dict.get, reverse=True)[:50]
        top_n_hashtags = sorted(popular_hashtags_dict, key=popular_hashtags_dict.get, reverse=True)[:50]
