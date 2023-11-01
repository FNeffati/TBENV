import re
import collections
from Locations import Locations


class Util:
    geo_tag_dict = collections.defaultdict(int)
    non_geo_hashtags_dict = collections.defaultdict(int)
    pure_locations = Locations().get_pure_locations("combined")
    categorized_locations = Locations().category_adder("combined")

    def extract_hashtags(self, sentence):
        result = []
        for word in sentence:
            if word[0] == '#' and word not in result:
                result.append(word)
        return result

    def geo_tag_harvester(self, list_of_hashtags):
        """
        This was made to look through a sentence at a time
        :param list_of_hashtags: an array of hashatags
        :return: None, it's a counter for location hashtags
        """
        pure_set = set(self.pure_locations[0])
        padded_set = set(self.categorized_locations[0])

        for word in list_of_hashtags:
            caught = False

            for word2 in pure_set:
                if word in word2.lower() or word2.lower() in word:
                    self.geo_tag_dict[word] += 1
                    caught = True
                    break  # Break the loop once caught

            if not caught:
                for word2 in padded_set:
                    if word in word2.lower():
                        self.geo_tag_dict[word] += 1
                        caught = True
                        break  # Break the loop once caught

            if not caught:
                self.non_geo_hashtags_dict[word] += 1

    def filter_hashtags(self, tokenized_sentence):
        """
        Function to filter all the stop words and the words that we deem unnecessary/misleading the statistics
        :param tokenized_sentence: a tokenized and partially cleaned text_column from the previous function
        :return: filtered lists of words that should capture the essence of what each row was about
        """
        result = []
        for w in tokenized_sentence:
            hashtag = w
            pure_word = re.sub(r"#", "", hashtag).lower()
            approved = True
            for word in Locations().get_stop_words(True):
                if word.lower() in pure_word:
                    approved = False
            if approved:
                result.append(pure_word.lower())

        return result

