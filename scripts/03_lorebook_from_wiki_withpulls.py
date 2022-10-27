# Imported Libraries
import pandas as pd
import re
import json
import uuid
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import wikipedia
from tqdm import tqdm
import datetime
import warnings
import random

warnings.filterwarnings("ignore") # reason we are ignoring the warning is because we are using the wikipedia package to get the content of the articles but we don't mind if we miss a few along the way. As it is right now, the process is designed to be slightly imperfect.

# Global Variables Declaration ------------------------------------------------
# get the list of names from the topics file
nltk.download("stopwords") #& download stopwords
stop_words = set(stopwords.words("english"))
maxlinksperpage = 30
minimum_key_occurrences = 4 # minimum number of times a keyword must appear in the text to be considered a keyword
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

# import the json file lorebook_example.lorebook
def examine_dates(entry1, entry2):
    # an article is useful if most of the dates in article A, fall within the max and min dates of article B with an error margin of 10 years.

    article_one_dates = []
    article_two_dates = []
    for sent in sent_tokenize(entry1):
        for chunk in nltk.ne_chunk(preprocess(sent)):
            if hasattr(chunk, "label"):
                if chunk.label() == "DATE":
                    article_one_dates.append(" ".join(c[0] for c in chunk.leaves()))
    for sent in sent_tokenize(entry2):
        for chunk in nltk.ne_chunk(preprocess(sent)):
            if hasattr(chunk, "label"):
                if chunk.label() == "DATE":
                    article_two_dates.append(" ".join(c[0] for c in chunk.leaves()))
    if len(article_one_dates) > 0 and len(article_two_dates) > 0:
        article_one_dates = [int(date) for date in article_one_dates if date.isdigit()]
        article_two_dates = [int(date) for date in article_two_dates if date.isdigit()]
        max_date = max(article_two_dates)
        min_date = min(article_two_dates)
        for date in article_one_dates:
            if date > max_date + 10 or date < min_date - 10:
                return False
        return True
    else:
        return False


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


def get_the_entities(content):
    # get the entities from the text
    entities = []
    for sent in sent_tokenize(content):
        for chunk in nltk.ne_chunk(preprocess(sent)):
            if hasattr(chunk, "label"):
                entities.append(" ".join(c[0] for c in chunk.leaves()))
    return entities


def generate_entries_from_list(list_of_names):
    # enter a list of people's names and get a list of entries, from wikipedia
    entries = []
    entry_names = []
    entry_keywords = []
    for name in tqdm(list_of_names):
        if name != "":
            try:
                entry = wikipedia.search(name)[
                    0
                ]  # get the first result from wikipedia, which is usually the most relevant
                page = wikipedia.page(entry)
                entry = page.content
                entry = re.sub(r"\([^)]*\)", " ", entry)  # remove anything in brackets
                # strip the text of all special characters, and any escaped characters using regex
                #!entry = re.sub(r'[^\w\s]',' ',entry)
                # remove any nonalpha characters
                entry = re.sub(r"[^a-zA-Z0-9,.?!'\;: ]", " ", entry).strip()
                entry = re.sub(r"\n", " ", entry)

                # \u patterns for unicode characters need to be removed, and replaced with the actual character
                # remove all unicode characters
                entry = re.sub(r"\\u[0-9a-fA-F]{4}", " ", entry)

                entry = re.sub(r"\\", " ", entry)
                entry = entry.replace("  ", " ")
                entry = entry.replace("  ", " ")
                entries.append(entry)
                # entry_keywords.append(get_the_entities(entry))
                # there may be related links in the wikipedia page, which we can also add to the list of keywords later
                related_links = page.links
                entry_keywords.append(related_links)
                entry_names.append(page.title)
            except:
                print("could not find entry for", name, " trying secondary search result instead")
                for xx in range(1, 5):
                    try:
                        entry = wikipedia.search(name)[
                            xx
                        ]  # get the second result from wikipedia, which is usually the most relevant
                        print(f'Looking at the {entry} page')
                        entries.append(entry)
                        entry_names.append(page.title)
                        # entry_keywords.append(entry_keywords)
                        break # break out of the loop if we find a result
                    except:
                        print("could not find summary for", name, " skipping")

    # generate fake ids for the entries in the format: 642723d1-a4a1-47a3-a63f-d36aee33de1b
    ids = []
    for i in range(len(entries)):
        ids.append(str(uuid.uuid4()))

    print("Entries generated")
    print(entry_names)
    print('--------------------------------')
    print(len(entry_keywords))
    print('--------------------------------')

    return entries, entry_names, ids, entry_keywords


def check_json_for_entry(entry_name, json_file):
    # check if an entry already exists in the json file
    with open(json_file, "r") as f:
        data = json.load(f)
    for entry in range(len(data["entries"])):
        if entry_name == "nan" or entry_name == "":
            continue
        if data["entries"][entry]["displayName"] == entry_name:
            print(f"{entry_name} - entry already exists", datetime.datetime.now())
            return True
    #print(f"{entry_name} - entry does not exist")
    return False

# def previous_main():

#     global context_config
#     # check those article pages for length (if they are too short, skip them)
#     # if they are long enough, and are not already in the list, add them to the list
#     list_of_names = pd.read_csv("./data/characters.csv")["Name"].tolist()
#     # print(type(list_of_names))
#     # list_of_names = [x[0] for x in list_of_names.values.tolist()]
#     # only keep names in the list of names that are not already in the json file
#     print("There are {} names in the list".format(len(list_of_names)))
#     print("Checking for names that already exist in the json file")
#     # list_of_names = [x for x in list_of_names if not check_json_for_entry(x, 'lorebook_generated.lorebook')]

#     # check a json file to see if any of the characters are already in the file, if they are, remove them from the list
#     # data['entries'][entry]['displayName'] == entry_name
#     # look for entries where the data['entries'][entry_number]['displayName'] is in the list of filenames
#     # if it is, remove it from the list
#     with open("./supporting_files/lorebook_generated.lorebook") as f:
#         data = json.load(f)
#         for entry in data["entries"]:
#             if entry["displayName"] in list_of_names:
#                 list_of_names.remove(entry["displayName"])

#     print(list_of_names[0:5])
#     print("There are {} names in the list".format(len(list_of_names)))
#     print("Generating entries from the list of names")

#     entries = []
#     entry_names = list_of_names














#     # for each Name
#     for name in tqdm(list_of_names):
#         if name != "":
#             try:
#                 entry = wikipedia.search(name)[
#                     0
#                 ]  # get the first result from wikipedia, which is usually the most relevant
#                 page = wikipedia.page(entry)
#                 entry = page.content
#                 links = page.links
#                 # remove duplicate links
#                 links = list(dict.fromkeys(links))
#                 # random sample of maxlinksperpage links
#                 links = random.sample(links, min(len(links), maxlinksperpage))
#                 print(f"Adding {name} to entries")
#                 # for link in tqdm(links):
#                 #     print(f'\nScanning {link}')

#                 #     # for every 2nd degree page
#                 #     if link.find('film')!=-1\
#                 #         or link.find('television')!=-1\
#                 #         or link.find('series')!=-1\
#                 #         or link.find('episode')!=-1\
#                 #         or link.find('century press')!=-1\
#                 #         or link.find('TV')!=-1:
#                 #             continue # skip film pages

#                 #         # skip religious pages
#                 #     if link.find('Christianity')!=-1\
#                 #         or link.find('Islam')!=-1\
#                 #         or link.find('Judaism')!=-1\
#                 #         or link.find('Buddhism')!=-1\
#                 #         or link.find('Hinduism')!=-1\
#                 #         or link.find('Sikhism')!=-1\
#                 #         or link.find('Atheism')!=-1\
#                 #         or link.find('Agnosticism')!=-1\
#                 #         or link.find('Religion')!=-1\
#                 #         or link.find('Religious')!=-1\
#                 #         or link.find('Jesus')!=-1\
#                 #         or link.find('God')!=-1\
#                 #         or link.find('Bible')!=-1\
#                 #         or link.find('Biblical')!=-1\
#                 #         or link.find(' cult ')!=-1\
#                 #         or link.find(' Cult ')!=-1\
#                 #         or link.find('Catholic')!=-1\
#                 #         or link.find('Protestant')!=-1\
#                 #         or link.find('Christian')!=-1\
#                 #         or link.find('Muslim')!=-1:
#                 #             continue # skip religious pages
#                 #     try:
#                 #         entry = wikipedia.search(link)[0] # get the first result from wikipedia, which is usually the most relevant
#                 #         page = wikipedia.page(entry)
#                 #         #!print(" length:", len(page.content))

#                 #         #!page.content = str(page.content).lower()
#                 #         if link not in entry_names and page.content != '' and len(page.content) > 5000 and \
#                 #             (page.content.find('Born')!=-1 and page.content.find('Family')!= -1): #// and (name.lower() in str(page.content).lower()):
#                 #             entries.append(page.content) #todo add examinedates
#                 #             entry_names.append(link)
#                 #             print(f' ==> Adding {link} to the list of entries')
#                 #             continue

#                 #         # if the page category contains "living people", "male _____", "female ____", or indicates that the page is about a person, then add it to the list of entries
#                 #         if page.categories != None and 'Living people' in page.categories \
#                 #             or 'male' in page.categories:
#                 #             entries.append(page.content)
#                 #             entry_names.append(link)
#                 #             print(f' ==> Adding {link} to the list of entries')
#                 #             continue
#                 #         # if is place
#                 #         if link not in entry_names and page.content != '' and len(page.content) > 5000 and (name.lower() in str(page.content).lower()) and (page.content.find('Geography')!=-1 and page.content.find('History')!=-1):# and page.content.find(r'Demographics|Demography')!=-1):
#                 #             entries.append(page.content)
#                 #             entry_names.append(link)
#                 #             print(f' ==> Adding LOC {link} to the list of entries')
#                 #             continue

#                 #     except Exception as e:
#                 #         pass

#             except Exception as e:
#                 print(e)
#                 continue
#         df = pd.DataFrame(entry_names)
#         # append to the csv file
#         prev_chars = pd.read_csv("./data/characters.csv")
#         # add the new characters to the list
#         prev_chars = prev_chars.append(df)
#         # remove duplicates
#         prev_chars = prev_chars.drop_duplicates()
#         # save the new list
#         prev_chars.to_csv("./data/characters.csv", index=False)
#         # # save entry_names to a csv
#         # df = pd.DataFrame(entry_names)
#         # df.to_csv('characters.csv', index=False)

#         with open("./supporting_files/lorebook_generated.lorebook") as f:
#             lore_dict = json.load(f)

#         topics_list = []
#         entry_keys = []
#         # input_text = 'start'
#         # while input_text != '':
#         #     input_text = input('Enter a topic: ')
#         #     topics_list.append(input_text)
#         # read in the list of topics from the characters.csv file
#         topics_list = pd.read_csv("./data/characters.csv")["Name"].tolist()
#         assert type(topics_list) == list  # make sure it's a list
#         # entries, entry_names = generate_entries_from_list(lore_dict['people'])

#         # generate only the entries in topics_list that are not already in the lorebook
#         # existing_topics = [entry['name'] for entry in lore_dict['entries']]
#         # topics_list = [x for x in topics_list if x not in lore_dict]

#         entries, entry_names, ids, entry_keywords = generate_entries_from_list(
#             topics_list
#         )
#         # add the entries to the lorebook dictionary. All we have to change is the text, display name, create a random id, and add the keys (which are the words in the text). All other fields can be copied from the first entry.

#         # create a list of the keys for each entry (all proper nouns, places and dates)
#         keys = []
#         keys_dict = {}
#         entry_id = 0
#         for entry in tqdm(entries):
#             print(f"Processing entry {entry[0:50]}...")
#             keys = []  # reset the keys list, so we don't have duplicate keys
#             for word, tag in tqdm(preprocess(entry)):
#                 if (
#                     (tag == "NNP" or tag == "NNPS" or tag == "CD")
#                     and word not in keys
#                     and word not in stop_words
#                     and len(word) > 2
#                 ):  # remove stop words, and numbers greater than 2020 (which are probably years)
#                     try:
#                         if int(word) < 2020:
#                             continue
#                     except:
#                         pass
#                     keys.append(word)
#             # add further keywords from the related links
#             for linklist in entry_keywords:
#                 for word in linklist:
#                     if word not in keys:
#                         keys.append(word)
#             prev_keys = keys  # get the previous keys
#             keys_dict[entry_id] = (
#                 prev_keys + entry_keys
#             )  # add the new keys to the previous keys
#             # remove dupe keys
#             res = []
#             for i in keys_dict[entry_id]:
#                 if i not in res:
#                     res.append(i)

#             # remove YouTube, Wikipedia, and other website links from res list
#             res = [i for i in res if not i.startswith("http")]
#             res = [i for i in res if not i.startswith("www")]
#             res = [i for i in res if not i.startswith("YouTube")]
#             res = [i for i in res if not i.startswith("Wikipedia")]
#             res = [i for i in res if not i.startswith("List")]

#             # remove stop words from res list
#             res = [i for i in res if not i in stop_words]
#             # remove words that are less than 4 characters
#             res = [i for i in res if len(i) > 3]
#             copy = res.copy()
#             copy = [i.lower() for i in copy]
#             res = [i for i in res if copy.count(i.lower()) < 2]
#             keys_dict[entry_id] = res
#             entry_id += 1



#         # add the entries to the lorebook dictionary

#         for i in range(len(entries)):
#             # append blanks to lore_dict['entries'] to make room for the new entries
#             try:
#                 lore_dict["entries"][i] = {}
#             except Exception as e:
#                 print(e)
#                 # lore_dict['entries'].append({'text': entries[i]})
#                 lore_dict["entries"].append({})

#         for i in tqdm(range(len(entries))):
#             # lore_dict > entries > text
#             # add a new entry to the lorebook dictionary
#             lore_dict["entries"][i]["text"] = str(entries[i])
#             # lore_dict > entries > contextConfig
#             lore_dict["entries"][i]["contextConfig"] = context_config
#             # lore_dict > entries > lastUpdatedAt
#             lore_dict["entries"][i]["lastUpdatedAt"] = 1649360732691
#             # lore_dict > entries > displayName
#             lore_dict["entries"][i]["displayName"] = entry_names[
#                 i
#             ]  # todo - was causing builtin method error for some reason in the final json file
#             # lore_dict > entries > id
#             lore_dict["entries"][i]["id"] = str(ids[i])
#             lore_dict["entries"][i]["searchRange"] = 10000
#             # lore_dict > entries > keys
#             lore_dict["entries"][i]["keys"] = keys_dict[i]  #
#             # *lore_dict['entries'][i]['keys'] = [] # blank for now
#         print(f"Saving {len(entries)} entries to lorebook")

#         # save the new lorebook dictionary as a json file called lorebook_generated.lorebook

#         # save the new lorebook dictionary as a json file called lorebook_generated.lorebook
#         with open("./supporting_files/lorebook_generated.lorebook", "w+") as f:
#             json.dump(lore_dict, f, indent=4)



def main():
    """
    main function - runs the program, processing the names provided in the characters.csv file and adding them to the lorebook_generated.lorebook file in the supporting_files folder. The function uses the generate_entries_from_list function to generate the entries, and then adds them to the lorebook_generated.lorebook file.
    """
    global context_config
    global minimum_key_occurrences

    # open the lorebook_generated.lorebook file
    try:
        with open("./supporting_files/lorebook_generated.lorebook") as f:
            lore_dict = json.load(f)
    except Exception as e:
        print(e)
        print("Error opening lorebook_generated.lorebook file")
        with open("./supporting_files/starter.lorebook") as f:
            lore_dict = json.load(f) # if the file doesn't exist, use the starter.lorebook file
    # check those article pages for length (if they are too short, skip them)
    # if they are long enough, and are not already in the list, add them to the list
    list_of_names = pd.read_csv("./data/characters.csv")["Name"].tolist()
    #* we need to be sure that none of the names are "None" or "nan"
    list_of_names = [x for x in list_of_names if str(x) != "nan"] # remove nan
    list_of_names = [x for x in list_of_names if str(x) != "None"] # remove None
    list_of_names = [x for x in list_of_names if str(x) != ""] # remove empty strings
    list_of_names = [x for x in list_of_names if str(x) != " "] # remove empty strings

    # only keep names in the list of names that are not already in the json file
    print("There are {} names in the list".format(len(list_of_names)))
    print("Checking for names that already exist in the json file")
    list_of_names = [x for x in list_of_names if not check_json_for_entry(x, './supporting_files/lorebook_generated.lorebook')]

    # check a json file to see if any of the characters are already in the file, if they are, remove them from the list
    # data['entries'][entry]['displayName'] == entry_name
    # look for entries where the data['entries'][entry_number]['displayName'] is in the list of filenames
    # if it is, remove it from the list
    with open("./supporting_files/lorebook_generated.lorebook") as f:
        data = json.load(f)
        for entry in data["entries"]:
            if entry["displayName"] in list_of_names:
                list_of_names.remove(entry["displayName"])

    print(list_of_names[0:5])
    print("There are {} names in the list".format(len(list_of_names)))
    print("Generating entries from the list of names")

    entries = []
    entry_names = list_of_names

    print(f'Generating entries for {len(entry_names)} names')
    print(entry_names)

    #!------------------------

    print(f'Processed {len(entry_names)} names')
    countnans = list_of_names.count('nan')
    print(f'Found {countnans} nan values')
    list_of_names = [x for x in entry_names if str(x) != 'nan']
    print(f'Removed {countnans} nan values')
    print(f'Processed {len(entry_names)} names')

    # for each Name
    for name in tqdm(list_of_names):
        keys = [] # list of keys for the entry
        if name != "":
            try:
                entry = wikipedia.search(name)[
                    0
                ]  # get the first result from wikipedia, which is usually the most relevant
                page = wikipedia.page(entry)
                entry = page.content
                links = page.links
                # remove duplicate links
                links = list(dict.fromkeys(links))
                # random sample of maxlinksperpage links
                links = random.sample(links, min(len(links), maxlinksperpage))
                print(f"Adding {name} to entries")
                entries.append(entry)
            except Exception as e:
                print(e)
                continue

        df = pd.DataFrame(entry_names)
        # append to the csv file
        #!prev_chars = pd.read_csv("./data/characters.csv")
        # add the new characters to the list
        #!prev_chars = prev_chars.append(df)
        # remove duplicates
        #!prev_chars = prev_chars.drop_duplicates()
        # save the new list
        #!prev_chars.to_csv("./data/characters.csv", index=False)
        # # save entry_names to a csv
        # df = pd.DataFrame(entry_names)
        # df.to_csv('characters.csv', index=False)

    with open("./supporting_files/lorebook_generated.lorebook") as f:
        lore_dict = json.load(f)

    # topics_list = []
    # entry_keys = []
    # input_text = 'start'
    # while input_text != '':
    #     input_text = input('Enter a topic: ')
    #     topics_list.append(input_text)
    # read in the list of topics from the characters.csv file
    # topics_list = pd.read_csv("./data/characters.csv")["Name"].tolist()
    # assert type(topics_list) == list  # make sure it's a list
    # entries, entry_names = generate_entries_from_list(lore_dict['people'])

    # generate only the entries in topics_list that are not already in the lorebook
    entries, entry_names, ids, entry_keywords = generate_entries_from_list(
        list_of_names
    )

    #!assert(len(entries) == len(entry_names), "The number of entries and entry names must be the same")
    # remove any entries that are already in the lorebook, or are only one word long
    #&entries = [x for x in entries if not check_json_for_entry(x, './supporting_files/lorebook_generated.lorebook')]
    entries = [x for x in entries if len(x.split()) > 1]
    # entry_names = [x for x in entry_names if not check_json_for_entry(x, './supporting_files/lorebook_generated.lorebook')]
    #!assert(len(entries) == len(entry_names), "after removing existing entries lengths are not the same") # make sure the lengths are the same
    # remove duplicates
    entries = list(dict.fromkeys(entries))

    # add the new entries to the lorebook
    for i in tqdm(range(len(entries))):
        #!print(f"\nAdding {entry_names[i]} to the lorebook")
        try:
            lore_dict['entries'].append({
                'displayName': list_of_names[i],
                'id': ids[i],
                'keywords': entry_keywords[i],
                'text': entries[i]
            })
            print(f"\nAdded {entry_names[i]} to the lorebook, with {len(entry_keywords[i])} keywords", end= ' ')
                # save the new lorebook
            with open("./supporting_files/lorebook_generated.lorebook", "w") as f:
                json.dump(lore_dict, f, indent=4)
            print(f' and saved progress...')
        except Exception as e:
            print(e)
            continue

    print(f"Saved {len(entries)} entries to the lorebook")

    # # for each entry print the number of keys in the keywords list
    # for entry in lore_dict['entries']:
    #     print(f'{entry["displayName"]} has {len(entry["keywords"])} keywords')

    # save the new lorebook dictionary as a json file called lorebook_generated.lorebook
    with open("./supporting_files/lorebook_generated.lorebook", "w+") as f:
        json.dump(lore_dict, f, indent=4)

def preview_lorebook(lorebook):
    # preview the lorebook by creating a pandas dataframe from the json file.
    # convert the lorebook object (json) to a pandas dataframe
    df = pd.DataFrame(lorebook)
    # print the first 5 rows of the dataframe
    print(df.head())




if __name__ == "__main__":
    main() # run the main function when the script is run
    print("Done")
    print("previewing the lorebook")
    with open("./supporting_files/lorebook_generated.lorebook") as f:
        lorebook = json.load(f)
    preview_lorebook(lorebook) # preview the lorebook