from pydoc_data.topics import topics
import pandas as pd
import json

import uuid
# import nltk
# nltk.download('punkt')
import nltk
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import wikipedia


stop_words = set(stopwords.words('english'))

# import the json file lorebook_example.lorebook


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def generate_entries_from_list(list_of_names):
    # enter a list of people's names and get a list of entries, from wikipedia
    entries = []
    entry_names = []
    for name in list_of_names:
        if name != '':
            try:
                entry = wikipedia.search(name)[0] # get the first result from wikipedia, which is usually the most relevant
                entries.append(entry)
                entry_names.append(entry.title)
            except:
                print('could not find entry for', name)
                try:
                    entry = wikipedia.search(name)[1] # get the second result from wikipedia, which is usually the most relevant
                    entries.append(entry)
                    entry_names.append(entry.title)
                except:
                    print('could not find summary for', name)


    # generate fake ids for the entries in the format: 642723d1-a4a1-47a3-a63f-d36aee33de1b
    ids = []
    for i in range(len(entries)):
        ids.append(str(uuid.uuid4()))
    return entries, entry_names, ids



## The goal: generate a lorebook dict from a list of text entries.
# list of text entries
# entries = [
#     'Testing 1',
#     'Testing 2',
#     'Testing 3'
# ]
# entry_names = [
#     'Test 1',
#     'Test 2',
#     'Test 3'
# ]

def main():


    with open('lorebook_example.lorebook') as f:
        lore_dict = json.load(f)

    topics_list = []
    input_text = 'start'
    while input_text != '':
        input_text = input('Enter a topic: ')
        topics_list.append(input_text)
    assert(type(topics_list) == list) # make sure it's a list
    # entries, entry_names = generate_entries_from_list(lore_dict['people'])
    entries, entry_names, ids = generate_entries_from_list(topics_list)
    # add the entries to the lorebook dictionary. All we have to change is the text, display name, create a random id, and add the keys (which are the words in the text). All other fields can be copied from the first entry.

    # create a list of the keys for each entry (all proper nouns, places and dates)
    keys = []
    for entry in entries:
        entry_keys = []
        for word, tag in preprocess(entry):
            if tag == 'NNP' or tag == 'NNPS' or tag == 'CD':
                entry_keys.append(word)
        keys.append(entry_keys)

    # keys update 2
    # add any words in the entry that are unique to that entry compared to all other entries in the lorebook
    for i in range(len(entries)):
        for j in range(len(entries)):
            if i != j:
                for word in entries[i].split():
                    if word not in entries[j].split() and word not in keys[i]:
                        keys[i].append(word)

    # add the entries to the lorebook dictionary
    for i in range(len(entries)):
        lore_dict['entries'].append({
            "text": entries[i],
            "contextConfig": {
            "prefix": "",
            "suffix": "\n",
            "tokenBudget": 2048,
            "reservedTokens": 0,
            "budgetPriority": 400,
            "trimDirection": "trimBottom",
            "insertionType": "newline",
            "maximumTrimType": "sentence",
            "insertionPosition": -1
            },
            "lastUpdatedAt": 1666044123984,
            "displayName": entry_names[i],
            "id": ids[i],
            "keys": keys[i],
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
                "whenInactive": False
            }
            ]
        })

    print(f'Saving {len(entries)} entries to lorebook')
    for entry in entries:
        print(f'I found {len(entry)} words for {entry}')
    # save the new lorebook dictionary as a json file called lorebook_generated.lorebook

    # save the new lorebook dictionary as a json file called lorebook_generated.lorebook
    with open('lorebook_generated.lorebook', 'w') as f:
        # lore_dict needs to be json serializable
        # this means that all the keys and values need to be strings
        # so we need to convert the keys and values to strings
        # we can do this with a dictionary comprehension
        lore_dict = {str(key): str(value) for key, value in lore_dict.items()}
        json.dump(lore_dict, f, indent=4)



main()