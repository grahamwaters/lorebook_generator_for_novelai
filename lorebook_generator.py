import pandas as pd
import numpy as np
import random
import wikipedia # wikipedia api
import json
from tqdm import tqdm
import uuid

context_config = {
    "prefix": "",
    "suffix": "\n",
    "tokenBudget": 100,  # max 2048
    "reservedTokens": 0,
    "budgetPriority": 400,
    "trimDirection": "trimBottom",
    "insertionType": "newline",
    "maximumTrimType": "sentence",
    "insertionPosition": -1,
}

def wikipedia_extractor(names):
    # given a person string (character), generate a lorebook for them from
    # pages on wikipedia for the character. The lorebook will be a dictionary

    lorebook = {}
    # get the wikipedia page for each name in names
    pages = []
    iterator = 0
    for name in names():
        iterator += 1








    iterator = 0
    for name in tqdm(names):
        # lore_dict > entries > text
        # add a new entry to the lorebook dictionary
        lorebook["entries"][iterator]["text"] = str(lorebook[iterator])
        # lore_dict > entries > contextConfig
    return lorebook


def main():
    # there is a list of characters/topics in several files in the data folder
    # we will use these to generate a lorebook for the novelai project

    # read in the files
    characters = pd.read_csv('entities_and_topics/characters.csv')


    # generate a lorebook for each character
    lorebook = wikipedia_extractor(characters)


    # save the lorebook to a json file
    lorebook.to_json('generated_lorebook.lorebook')

if __name__ == '__main__':
    main()





# lorebook = pd.DataFrame() # initialize the lorebook with the following architecture: lorebook['entries']['row_number']['text']
#     topics_list = pd.read_csv("characters.csv")["Name"].tolist()
#     for i in range(len(topics_list)):
#         # append blanks to lorebook['entries'] to make room for the new entries
#         try:
#             lorebook["entries"][i] = {}
#         except Exception as e:
#             print(e)
#             # lorebook['entries'].append({'text': entries[i]})
#             lorebook["entries"].append({})

#     for i in tqdm(range(len(topics_list))):
#         # lore_dict > entries > text
#         # add a new entry to the lorebook dictionary
#         lorebook["entries"][i]["text"] = str(lorebook[i])
#         # lore_dict > entries > contextConfig
#         lorebook["entries"][i]["contextConfig"] = context_config
#         # lore_dict > entries > lastUpdatedAt
#         lorebook["entries"][i]["lastUpdatedAt"] = 1649360732691
#         # lore_dict > entries > displayName
#         lorebook["entries"][i]["displayName"] = entry_names[i]  # todo - was causing builtin method error for some reason in the final json file
#         # lore_dict > entries > id
#         lorebook["entries"][i]["id"] = str(ids[i])
#         # lore_dict > entries > keys
#         lorebook["entries"][i]["keys"] = keys_dict[i]  #