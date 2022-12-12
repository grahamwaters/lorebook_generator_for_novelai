from typing import Tuple
from uuid import uuid4
import nltk
from typing import Tuple
import json

from nltk.corpus import stopwords


def get_keywords(text, stopwords, n_keys):  #  -> Tuple[list, str]:

    """
    Extract keywords from text
    :param text: text to extract keywords from
    :param stopwords: list of stopwords to filter out
    :param n_keys: number of keywords to extract
    :return: list of keywords and the text
    """

    n_keys = int(n_keys)  # cast the n_keys to an integer
    text = text.strip().lower()
    words = text.split()
    keyword_counts = {}
    keyword_counts = {word: keyword_counts.get(word, 0) + 1 for word in words}
    sorted_keywords = sorted(keyword_counts, key=keyword_counts.get, reverse=True)
    # Filter the sorted keywords to only include words that are more than 3 characters long and are not in the stopwords list
    filtered_keywords = list(
        [word for word in sorted_keywords if len(word) > 3 and word not in stopwords]
    )
    return filtered_keywords[:n_keys], text


# place holders
text = ""  # enter text here
sorted_keywords = []  # enter keywords here
# n_keys = 20 # enter number of keywords here

data_template_dict = {
    "lorebookVersion": 4,
    "entries": [
        {
            "text": text,
            "contextConfig": {
                "prefix": "",
                "suffix": "\n",
                "tokenBudget": 2048,
                "reservedTokens": 0,
                "budgetPriority": 400,
                "trimDirection": "trimBottom",
                "insertionType": "newline",
                "maximumTrimType": "sentence",
                "insertionPosition": -1,
            },
            "lastUpdatedAt": 1666846259188,
            "displayName": "New Lorebook Entry",
            "id": "bd90161f-4ff6-44a0-8522-0f25ad26aae3",
            "keys": sorted_keywords[:20],
            "searchRange": 1000,
            "enabled": True,
            "forceActivation": False,
            "keyRelative": False,
            "nonStoryActivatable": False,
            "category": "",
            "loreBiasGroups": [
                {
                    "phrases": [],
                    "ensureSequenceFinish": False,
                    "generateOnce": True,
                    "bias": 0,
                    "enabled": True,
                    "whenInactive": False,
                }
            ],
        }
    ],
    "settings": {"orderByKeyLocations": False},
    "categories": [],
}

##########
text = input("Enter text: ")

##########
stopwords = set(stopwords.words("english"))
number_of_keywords = 20
sorted_keywords, text = get_keywords(text, stopwords, number_of_keywords)

# get the keywords
data_dict = data_template_dict.copy()  # create a copy of the data_template_dict

# update the data dictionary's keywords and text with the formatting of data_template_dict
sorted_keywords = get_keywords(text, stopwords, number_of_keywords)[
    0
]  # get the keywords
data_dict["keywords"] = sorted_keywords[:number_of_keywords]  # update the keywords
data_dict["entries"][0]["text"] = text
data_dict["entries"][0]["searchRange"] = 10_000  # update the search range to 10,000
data_dict["entries"][0]["id"] = str(uuid4().int)  # update the keys
# add the name of the entry
data_dict["entries"][0]["displayName"] = text[0:10] + "..."

# save the data_template_dict to a json file
with open("data_template.json", "w") as f:
    json.dump(data_template_dict, f, indent=2)


print(data_dict)
