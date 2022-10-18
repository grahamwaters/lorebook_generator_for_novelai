import pandas as pd
import numpy as np
import os
import json, uuid
import tqdm
# from main import *
from main import check_json_for_entry, entries, master_list_of_names, preprocess, stop_words


# open the characters file and save it as a list of characters
def open_characters():
    with open("characters.csv", "r") as f:
        characters = f.read().splitlines()
    return characters

list_of_names_f = open_characters()

with open('lorebook_generated.lorebook') as f:
    lore_dict = json.load(f)

topics_list = [x for x in list_of_names_f if not check_json_for_entry(x, 'lorebook_generated.lorebook')]



entry_keys = []
for entry in entries:
    topics_list.append(entry)
    entry_keys.append(str(uuid.uuid4()))


assert(type(topics_list) == list) # make sure it's a list
# entries, entry_names = generate_entries_from_list(lore_dict['people'])

# generate only the entries in topics_list that are not already in the lorebook
#existing_topics = [entry['name'] for entry in lore_dict['entries']]
#topics_list = [x for x in topics_list if x not in lore_dict]

entries, entry_names, ids,entry_keywords = generate_entries_from_list(master_list_of_names)
# add the entries to the lorebook dictionary. All we have to change is the text, display name, create a random id, and add the keys (which are the words in the text). All other fields can be copied from the first entry.

# create a list of the keys for each entry (all proper nouns, places and dates)
keys = []
keys_dict = {}
entry_id = 0
for entry in tqdm(entries):
    print(f'Processing entry {entry[0:50]}...')
    keys = [] # reset the keys list, so we don't have duplicate keys
    for word, tag in tqdm(preprocess(entry)):
        if (tag == 'NNP' or tag == 'NNPS' or tag == 'CD') and word not in keys\
            and word not in stop_words and len(word) > 2: # remove stop words, and numbers greater than 2020 (which are probably years)
            try:
                if int(word) < 2020:
                    continue
            except:
                pass
            keys.append(word)
    # add further keywords from the related links
    for linklist in entry_keywords:
        for word in linklist:
            if word not in keys:
                keys.append(word)
    prev_keys = keys # get the previous keys
    keys_dict[entry_id] = prev_keys + entry_keys # add the new keys to the previous keys
    # remove dupe keys
    res = []
    for i in keys_dict[entry_id]:
        if i not in res:
            res.append(i)



    # remove YouTube, Wikipedia, and other website links from res list
    res = [i for i in res if not i.startswith('http')]
    res = [i for i in res if not i.startswith('www')]
    res = [i for i in res if not i.startswith('YouTube')]
    res = [i for i in res if not i.startswith('Wikipedia')]
    res = [i for i in res if not i.startswith('List')]

    # remove stop words from res list
    res = [i for i in res if not i in stop_words]
    # remove words that are less than 4 characters
    res = [i for i in res if len(i) > 3]
    copy = res.copy()
    copy = [i.lower() for i in copy]
    res = [i for i in res if copy.count(i.lower()) < 2]
    keys_dict[entry_id] = res
    entry_id += 1




context_config = {
        "prefix": "",
        "suffix": "\n",
        "tokenBudget": 100, # max 2048
        "reservedTokens": 0,
        "budgetPriority": 400,
        "trimDirection": "trimBottom",
        "insertionType": "newline",
        "maximumTrimType": "sentence",
        "insertionPosition": -1
    }

# add the entries to the lorebook dictionary

for i in range(len(entries)):
    # append blanks to lore_dict['entries'] to make room for the new entries
    try:
        lore_dict['entries'][i] = {}
    except Exception as e:
        print(e)
        #lore_dict['entries'].append({'text': entries[i]})
        lore_dict['entries'].append({})

for i in tqdm(range(len(entries))):
    # lore_dict > entries > text
    # add a new entry to the lorebook dictionary
    lore_dict['entries'][i]['text'] = str(entries[i])
    # lore_dict > entries > contextConfig
    lore_dict['entries'][i]['contextConfig'] = context_config
    # lore_dict > entries > lastUpdatedAt
    lore_dict['entries'][i]['lastUpdatedAt'] = 1649360732691
    # lore_dict > entries > displayName
    lore_dict['entries'][i]['displayName'] = entry_names[i] # todo - was causing builtin method error for some reason in the final json file
    # lore_dict > entries > id
    lore_dict['entries'][i]['id'] = str(ids[i])
    # lore_dict > entries > keys
    lore_dict['entries'][i]['keys'] = keys_dict[i] #
    #*lore_dict['entries'][i]['keys'] = [] # blank for now
print(f'Saving {len(entries)} entries to lorebook')

# save the new lorebook dictionary as a json file called lorebook_generated.lorebook

# save the new lorebook dictionary as a json file called lorebook_generated.lorebook
with open('lorebook_generated.lorebook', 'w+') as f:
    json.dump(lore_dict, f, indent=4)
