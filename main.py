from pydoc_data.topics import topics
import pandas as pd
import json
import re
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
import tqdm
from tqdm import tqdm
import datetime

# set set_rate_limiting to True to avoid getting blocked by wikipedia
wikipedia.set_rate_limiting(True)

stop_words = set(stopwords.words('english'))

# import the json file lorebook_example.lorebook


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def get_the_entities(content):
    # get the entities from the text
    entities = []
    for sent in sent_tokenize(content):
        for chunk in nltk.ne_chunk(preprocess(sent)):
            if hasattr(chunk, 'label'):
                entities.append(' '.join(c[0] for c in chunk.leaves()))
    return entities

def generate_entries_from_list(list_of_names):
    # enter a list of people's names and get a list of entries, from wikipedia
    entries = []
    entry_names = []
    entry_keywords = []
    for name in tqdm(list_of_names):
        if name != '':
            try:
                entry = wikipedia.search(name)[0] # get the first result from wikipedia, which is usually the most relevant
                page = wikipedia.page(entry)
                entry = page.content
                entry = re.sub(r'\([^)]*\)', ' ', entry) # remove anything in brackets
                # strip the text of all special characters, and any escaped characters using regex
                #!entry = re.sub(r'[^\w\s]',' ',entry)
                # remove any nonalpha characters
                entry = re.sub(r"[^a-zA-Z0-9,.?!'\;: ]",' ',entry).strip()
                entry = re.sub(r'\n',' ',entry)

                # \u patterns for unicode characters need to be removed, and replaced with the actual character
                # remove all unicode characters
                entry = re.sub(r'\\u[0-9a-fA-F]{4}',' ',entry)


                entry = re.sub(r'\\',' ',entry)
                entry = entry.replace('  ', ' ')
                entry = entry.replace('  ', ' ')
                entries.append(entry)
                entry_names.append(page.title)
                # entry_keywords.append(get_the_entities(entry))
                # there may be related links in the wikipedia page, which we can also add to the list of keywords later
                related_links = page.links
                entry_keywords.append(related_links)
            except:
                print('could not find entry for', name)
                try:
                    entry = wikipedia.search(name)[1] # get the second result from wikipedia, which is usually the most relevant
                    entries.append(entry)
                    entry_names.append(page.title)
                    # entry_keywords.append(entry_keywords)
                except:
                    print('could not find summary for', name)


    # generate fake ids for the entries in the format: 642723d1-a4a1-47a3-a63f-d36aee33de1b
    ids = []
    for i in range(len(entries)):
        ids.append(str(uuid.uuid4()))
    return entries, entry_names, ids,entry_keywords

layer = 0
topics_list = []

with open('starter.lorebook') as f:
    lore_dict = json.load(f)

def main():
    global layer
    entry_keys = []
    input_text = 'start'
    while input_text != '':
        input_text = input('Enter a topic: ')
        topics_list.append(input_text)
    assert(type(topics_list) == list) # make sure it's a list
    # entries, entry_names = generate_entries_from_list(lore_dict['people'])
    entries, entry_names, ids,entry_keywords = generate_entries_from_list(topics_list)
    # add the entries to the lorebook dictionary. All we have to change is the text, display name, create a random id, and add the keys (which are the words in the text). All other fields can be copied from the first entry.

    # create a list of the keys for each entry (all proper nouns, places and dates)
    keys = []
    keys_dict = {}
    secondary_pages_master = []
    entry_id = 0
    for entry in entries:
        keys = [] # reset the keys list, so we don't have duplicate keys
        for word, tag in preprocess(entry):
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
            secondary_pages = linklist # get the list of related links
            secondary_pages_master.append(secondary_pages)
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

    # go through the secondary pages check them for names of people, only keep names of people.

    for pages in secondary_pages_master:
        for page in pages:
            # check if the page is a person with nltk
            if nltk.pos_tag(nltk.word_tokenize(page))[0][1] == 'NNP':
                # if it is a person, add it to the list of topics
                topics_list.append(page) # add the page to the list of topics
                if layer == 0: layer = 1 # if this is the first layer, set the layer to 1
                else: layer = 2 # if this is the second layer, set the layer to 2
    if layer == 1:
        main() # if the layer is 1, run the main function again
    else:
        pass




    context_config = {
            "prefix": "",
            "suffix": "\n",
            "tokenBudget": 2048,
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
        lore_dict['entries'].append({})

    for i in range(len(entries)):
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


main()