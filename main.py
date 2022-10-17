import pandas as pd
import json


# import nltk
# nltk.download('punkt')
import nltk
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

stop_words = set(stopwords.words('english'))

# import the json file lorebook_example.lorebook
with open('Ripple (Mon Oct 17 2022).lorebook') as f:
    lore_dict = json.load(f)


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent





## The goal: generate a lorebook dict from a list of text entries.
# list of text entries
entries = [
    'Testing 1',
    'Testing 2',
    'Testing 3'
]
entry_names = [
    'Test 1',
    'Test 2',
    'Test 3'
]








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