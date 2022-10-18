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

stop_words = set(stopwords.words('english'))

# import the json file lorebook_example.lorebook

"""
    "Nikola Tesla",
"Thomas Edison",
"George Westinghouse",
"Alexander Graham Bell",
"Samuel Morse",
"Benjamin Franklin",
"Guglielmo Marconi",
"London",
"Paris",
"New York",
"Washington DC",
"Berlin, Germany",
"West Berlin",
"East Berlin",
"Hitler",
"Joseph Stalin",
"Franklin D. Roosevelt",
"Harry S. Truman",
"Queen Victoria",
"Charles Dickens",
"William Shakespeare",
"Jules Verne",
"Samuel Clemens",
"Charles Darwin",
"Albert Einstein",
"Isaac Newton",
"Leonardo da Vinci",
"Captain James Cook",
"Wardenclyffe Tower",
"Famous Scientists",
"Famous Paintings",
"Mythical Creatures",
"World War 1",
"World War 2",
"Western Front",
"List_of_people_who_disappeared_mysteriously:_pre-1910",
"List_of_people_who_disappeared_mysteriously:_1910-1949",
"List_of_people_who_disappeared_mysteriously:_1950-1999",
"List_of_people_who_disappeared_mysteriously:_2000-present",

    _extended_summary_
"""

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
# get all links on each of the entity pages
from tqdm import tqdm
import pandas as pd
import wikipedia

def main():




    # check those article pages for length (if they are too short, skip them)
    # if they are long enough, and are not already in the list, add them to the list
    list_of_names = pd.read_csv('characters.csv')
    print(type(list_of_names))
    list_of_names = list_of_names['Name'].tolist()
    entries = []
    entry_names = []
    for name in tqdm(list_of_names):
        if name != '':
            try:
                entry = wikipedia.search(name)[0] # get the first result from wikipedia, which is usually the most relevant
                page = wikipedia.page(entry)
                entry = page.content
                links = page.links
                print(f'Adding {name} to entries')
                for link in tqdm(links):
                    #print("Checking link ", link,end='')
                    # for every 2nd degree page
                    try:
                        entry = wikipedia.search(link)[0] # get the first result from wikipedia, which is usually the most relevant
                        page = wikipedia.page(entry)
                        #!print(" length:", len(page.content))
                        if link not in entry_names and page.content != '' and len(page.content) > 5000 and (name in page.content or page.content.find('born ')!=-1): # if the page is long enough and not already in the list, add it
                            entries.append(page.content)
                            entry_names.append(link)
                            print(f' ==> Adding {link} to the list of entries')
                    except:
                        pass
            except Exception as e:
                print(e)
                continue
        df = pd.DataFrame(entry_names)
        df.to_csv('characters.csv', index=False) # save the list of entries

    # save entry_names to a csv
    df = pd.DataFrame(entry_names)
    df.to_csv('characters.csv', index=False)














    with open('lorebook_generated.lorebook') as f:
        lore_dict = json.load(f)

    topics_list = []
    entry_keys = []
    # input_text = 'start'
    # while input_text != '':
    #     input_text = input('Enter a topic: ')
    #     topics_list.append(input_text)
    # read in the list of topics from the characters.csv file
    topics_list = pd.read_csv('characters.csv')['Name'].tolist()
    assert(type(topics_list) == list) # make sure it's a list
    # entries, entry_names = generate_entries_from_list(lore_dict['people'])

    # generate only the entries in topics_list that are not already in the lorebook
    #existing_topics = [entry['name'] for entry in lore_dict['entries']]
    #topics_list = [x for x in topics_list if x not in lore_dict]

    entries, entry_names, ids,entry_keywords = generate_entries_from_list(topics_list)
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


main()