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
import warnings
import os

warnings.filterwarnings(
    "ignore"
)  # reason we are ignoring the warning is because we are using the wikipedia package to get the content of the articles but we don't mind if we miss a few along the way. As it is right now, the process is designed to be slightly imperfect.

# Global Variables Declaration ------------------------------------------------
# get the list of names from the topics file
nltk.download("stopwords")  # & download stopwords
stop_words = set(stopwords.words("english"))
maxlinksperpage = 30


# * Import Configuration Dictionary from scripts/lorebook_params.py file
# goal: eventually have an external file for these variables
context_config = {
    "prefix": "",
    "suffix": "\n",
    "tokenBudget": 200,  # max 2048
    "reservedTokens": 0,
    "budgetPriority": 400,
    "trimDirection": "trimBottom",
    "insertionType": "newline",
    "maximumTrimType": "sentence",
    "insertionPosition": -1,
}

# * Import helper functions from scripts/helpers.py file
# import the helper functions from the helpers.py file
from helpers import *


# Functions for generating the lorebook

# Functions for generating the lorebook
# def preprocess(sent):
#     """
#     preprocess the text to remove stopwords and punctuation

#     This function is used to preprocess the text before it is fed into the named entity recognition algorithm.

#     :param sent: the text to be preprocessed
#     :type sent: str
#     :return: the preprocessed text
#     :rtype: str
#     """
#     sent = nltk.word_tokenize(sent)
#     sent = nltk.pos_tag(sent)
#     return sent

# def get_the_entities(content):
#     """
#     get_the_entities is a function that uses the nltk library to extract the named entities from a text.

#     This function uses the nltk library to extract the named entities from a text. It uses the nltk library to preprocess the text, and then uses the nltk library to extract the named entities from the text. It returns a list of the named entities.

#     :param content: the text to extract the named entities from
#     :type content:  str
#     :return: a list of the named entities
#     :rtype: list
#     """
#     # get the entities from the text
#     entities = []
#     for sent in sent_tokenize(content):
#         for chunk in nltk.ne_chunk(preprocess(sent)):
#             if hasattr(chunk, "label"):
#                 entities.append(" ".join(c[0] for c in chunk.leaves()))
#     return entities

# def generate_entries_from_list(list_of_names):
#     # enter a list of people's names and get a list of entries, from wikipedia
#     """
#     generate_entries_from_list is a function that generates a list of entries from a list of names.

#     This function generates a list of entries from a list of names. It uses the wikipedia library to get the wikipedia page for each name, and then extracts the text from the wikipedia page. It then returns a list of the entries.

#     :param list_of_names: a list of names
#     :type list_of_names: list
#     :return: a list of entries
#     :rtype: list
#     """
#     entries = []
#     entry_names = []
#     entry_keywords = []
#     for name in tqdm(list_of_names):
#         if name != "":
#             try:
#                 entry = wikipedia.search(name)[
#                     0
#                 ]  # get the first result from wikipedia, which is usually the most relevant
#                 page = wikipedia.page(entry)
#                 entry = page.content
#                 entry = re.sub(r"\([^)]*\)", " ", entry)  # remove anything in brackets
#                 # strip the text of all special characters, and any escaped characters using regex
#                 #!entry = re.sub(r'[^\w\s]',' ',entry)
#                 # remove any nonalpha characters
#                 entry = re.sub(r"[^a-zA-Z0-9,.?!'\;: ]", " ", entry).strip()
#                 entry = re.sub(r"\n", " ", entry)

#                 # \u patterns for unicode characters need to be removed, and replaced with the actual character
#                 # remove all unicode characters
#                 entry = re.sub(r"\\u[0-9a-fA-F]{4}", " ", entry)

#                 entry = re.sub(r"\\", " ", entry)
#                 entry = entry.replace("  ", " ")
#                 entry = entry.replace("  ", " ")
#                 entries.append(entry)
#                 entry_names.append(page.title)
#                 # entry_keywords.append(get_the_entities(entry))
#                 # there may be related links in the wikipedia page, which we can also add to the list of keywords later
#                 related_links = page.links
#                 entry_keywords.append(related_links)
#             except:
#                 print("could not find entry for", name)
#                 try:
#                     entry = wikipedia.search(name)[
#                         1
#                     ]  # get the second result from wikipedia, which is usually the most relevant
#                     entries.append(entry)
#                     entry_names.append(page.title)
#                     # entry_keywords.append(entry_keywords)
#                 except:
#                     print("could not find summary for", name)

#     # generate fake ids for the entries in the format: 642723d1-a4a1-47a3-a63f-d36aee33de1b
#     ids = []
#     for i in range(len(entries)):
#         ids.append(str(uuid.uuid4()))
#     return entries, entry_names, ids, entry_keywords


# def create_keys(entries):
#     # create a list of the keys for each entry (all proper nouns, places and dates)
#     keys = []
#     try:  # try to open the keys dict csv file
#         keys_dict = pd.read_csv("keys_dict.csv").set_index("id").to_dict()["keys"]
#         entry_id = len(keys_dict)
#     except Exception as e:
#         print(e)
#         keys_dict = {}
#         entry_id = 0
#     # keys_dict = {}

#     for entry in tqdm(entries):
#         #!print(f'Processing entry {entry[0:50]}...')
#         print(f"Processing entry {entry[0:50]}...")
#         keys = []  # reset the keys list, so we don't have duplicate keys
#         for word, tag in preprocess(entry):
#             if (
#                 (tag == "NNP" or tag == "NNPS" or tag == "CD")
#                 and word not in keys
#                 and word not in stop_words
#                 and len(word) > 2
#                 and word != "Gregorian"
#             ):  # remove stop words, and numbers greater than 2020 (which are probably years)
#                 try:
#                     if int(word) < 2020:
#                         continue
#                 except:
#                     pass
#                 keys.append(word)

#             if len(keys) > 50:
#                 break

#         # add further keywords from the related links
#         # for linklist in entry_keywords:
#         #     for word in linklist:
#         #         if word not in keys:
#         #             keys.append(word)
#         # prev_keys = keys # get the previous keys
#         try:
#             keys_dict[entry_id] = (
#                 prev_keys + entry_keys
#             )  # add the new keys to the previous keys
#         except:
#             keys_dict[entry_id] = keys
#         # remove dupe keys
#         res = []
#         for i in keys_dict[entry_id]:
#             if i not in res:
#                 res.append(i)

#         # remove YouTube, Wikipedia, and other website links from res list
#         res = [i for i in res if not i.startswith("http")]
#         res = [i for i in res if not i.startswith("www")]
#         res = [i for i in res if not i.startswith("YouTube")]
#         res = [i for i in res if not i.startswith("Wikipedia")]
#         res = [i for i in res if not i.startswith("List")]

#         # remove stop words from res list
#         res = [i for i in res if not i in stop_words]
#         # remove words that are less than 4 characters
#         res = [i for i in res if len(i) > 3]
#         copy = res.copy()
#         copy = [i.lower() for i in copy]
#         res = [
#             i for i in res if copy.count(i.lower()) < 2
#         ]  # remove duplicate keys, but keep the case
#         keys_dict[entry_id] = res  # update the keys dict
#         entry_id += 1  # increment the entry id

#         # add bigrams that are unique to this entry (compared to the other entries) to the keys list
#         # bigrams = list(nltk.bigrams(entry.split()))
#         # for bigram in bigrams:
#         #     if bigram not in keys and bigram not in stop_words:
#         #         keys.append(bigram)

#         if entry_id % 100 == 0:
#             print(f"Processed {entry_id} entries")
#             # save the keys_dict to a pandas dataframe, and save it to a csv file
#             df = pd.DataFrame.from_dict(keys_dict, orient="index")
#             df.to_csv("keys_dict.csv")
#             print("Saved keys_dict.csv")

#     return keys_dict

# def generate_lorebook(
#     lore_dict, characters, entries, entry_names, ids, years_list, topics_scanner_list
# ):

#     # add the entries to the lorebook dictionary. All we have to change is the text, display name, create a random id, and add the keys (which are the words in the text). All other fields can be copied from the first entry.
#     keys_dict = create_keys(
#         entries
#     )  # create the keys for each entry in the entries list
#     global context_config

#     for i in range(len(entries)):
#         # append blanks to lore_dict['entries'] to make room for the new entries
#         try:
#             lore_dict["entries"][i] = {}
#         except Exception as e:
#             print(e)
#             # lore_dict['entries'].append({'text': entries[i]})
#             lore_dict["entries"].append({})
#     for i in tqdm(range(len(entries))):
#         # lore_dict > entries > text
#         # add a new entry to the lorebook dictionary
#         lore_dict["entries"][i]["text"] = str(entries[i])
#         # lore_dict > entries > contextConfig
#         lore_dict["entries"][i]["contextConfig"] = context_config
#         # lore_dict > entries > lastUpdatedAt
#         lore_dict["entries"][i]["lastUpdatedAt"] = 1649360732691
#         # lore_dict > entries > displayName
#         lore_dict["entries"][i]["displayName"] = entry_names[i]
#         # lore_dict > entries > id
#         lore_dict["entries"][i]["id"] = str(uuid.uuid4())
#         lore_dict["entries"][i]["searchRange"] = 10000
#         # lore_dict > entries > keys
#         # update keys_dict[i] to include the display name of the entry, and the years_list, and the topics_scanner_list
#         # keys_dict[i].append(entry_names[i])
#         keys_dict[i].extend(years_list)
#         keys_dict[i].extend(topics_scanner_list)
#         # keys_dict[i].extend(entry_names[i])
#         lore_dict["entries"][i]["keys"] = keys_dict[i]  #
#         # *lore_dict['entries'][i]['keys'] = [] # blank for now

#         if i % 100 == 0:
#             # save the new lorebook dictionary as a json file called lorebook_generated.lorebook
#             print(f"Saving at entry {i} to lorebook")
#             with open("lorebook_generated.lorebook", "w+") as f:
#                 json.dump(lore_dict, f, indent=4)
#     print(f"Saving {len(entries)} entries to lorebook")

#     # save the new lorebook dictionary as a json file called lorebook_generated.lorebook
#     with open("lorebook_generated.lorebook", "w+") as f:
#         json.dump(lore_dict, f, indent=4)


def main():
    # generate a lorebook.lorebook file from the articles (text files) in the wikipedia_pages directory.
    # Files:
    # lorebook_example.lorebook - the example lorebook file
    # lorebook_generated.lorebook - the generated lorebook file
    # characters.csv - a list of characters to generate entries for (one per line)
    # wikipedia_pages - a directory containing the text files of wikipedia articles to generate entries from (one per file), entry name will be the filename

    # read in the lorebook_generated.lorebook file (if it exists)
    try:
        with open("./supporting_files/lorebook_generated.lorebook", "r") as f:
            lore_dict = json.load(f)
    except:
        lore_dict = {}

    # read in the characters.csv file
    with open("./data/characters.csv", "r") as f:
        characters = f.read().splitlines()

    # read in the wikipedia pages from each file in the wikipedia_pages directory
    # each file is a wikipedia article, and the entry name will be the filename
    # the text from each file will be added to the entries list
    # the entry name will be added to the entry_names list
    # the entry id will be added to the ids list
    entries = []
    entry_names = []
    ids = []

    # define topics list
    topics_scanner_list = []  # initialize the topics_scanner_list
    # Ask for a topic to scan docs for
    print("What year would you like to scan for?")
    print("Type Return when finished")
    print(
        f'   this will scan all {len(os.listdir("wikipedia_pages"))} docs for the topics you enter'
    )
    years_list = []
    while True:
        inp = input("Topic: ")
        if inp == "":
            break
        else:
            # if the input is a year (4 digits), add it to the years_list instead of the topics_scanner_list
            if inp.isdigit() and len(inp) == 4:
                years_list.append(str(inp))
            else:
                print("Detected a topic and added to the right list...")
                topics_scanner_list.append(inp)

    print(f"Will scan for the years: {years_list}")
    print(
        f"Are there topics, people, places, or events you want to find to narrow the search?"
    )
    print("Note: this will return docs that contain (ANY) of the topics you enter")
    mode = input(
        'Type "all" if all terms must be in the same document, or "any" if they can be in some but not in others: '
    )
    while True:
        inp = input("Topic: ")
        if inp == "":
            break
        else:
            topics_scanner_list.append(inp)

    # //file_mode(mode,topics_scanner_list,years_list)
    print("Scanning for topics...")

    for filename in tqdm(os.listdir("./wikipedia_pages")):
        if filename == ".DS_Store":
            continue  # skip the .DS_Store file
        with open(f"./wikipedia_pages/{filename}", "r") as f:
            f_rd = f.read()
            if mode == "any":
                # check if the file contains any of the topics in the topics_scanner_list
                if any(
                    topic.lower() in f_rd.lower() for topic in topics_scanner_list
                ) and any(year.lower() in f_rd.lower() for year in years_list):
                    entries.append(f_rd)
                    entry_names.append(filename)
                    ids.append(str(uuid.uuid4()))
            elif mode == "all":
                # check if the file contains all of the topics in the topics_scanner_list
                if all(
                    topic.lower() in f_rd.lower() for topic in topics_scanner_list
                ) and all(year.lower() in f_rd.lower() for year in years_list):
                    entries.append(f_rd)
                    entry_names.append(filename)
                    ids.append(str(uuid.uuid4()))
            else:
                print("Invalid mode, exiting...")
                return

    #!web_mode(entry_names) # comment this out if you don't want to use the web mode
    # generate the lorebook
    lore_dict = generate_lorebook(
        lore_dict,
        characters,
        entries,
        entry_names,
        ids,
        years_list,
        topics_scanner_list,
    )
    print("Done")


def file_mode(mode, topics_scanner_list, years_list):
    global entries
    global entry_names
    global ids

    # global mode
    print("Scanning for topics...")

    for filename in tqdm(os.listdir("./wikipedia_pages")):
        if filename == ".DS_Store":
            continue  # skip the .DS_Store file
        with open(f"./wikipedia_pages/{filename}", "r") as f:
            f_rd = f.read()
            if mode == "any":
                # check if the file contains any of the topics in the topics_scanner_list
                if any(
                    topic.lower() in f_rd.lower() for topic in topics_scanner_list
                ) and any(year.lower() in f_rd.lower() for year in years_list):
                    entries.append(f_rd)
                    entry_names.append(filename)
                    ids.append(str(uuid.uuid4()))
            elif mode == "all":
                # check if the file contains all of the topics in the topics_scanner_list
                if all(
                    topic.lower() in f_rd.lower() for topic in topics_scanner_list
                ) and all(year.lower() in f_rd.lower() for year in years_list):
                    entries.append(f_rd)
                    entry_names.append(filename)
                    ids.append(str(uuid.uuid4()))
            else:
                print("Invalid mode, exiting...")
                return


# note: web_mode is in dev. Nonoperational as of 10/26/22
def web_mode(entry_names):
    # use the wikipedia api to get the text of the wikipedia pages instead of reading them from files.
    # this is slower, but it will get the latest version of the page.
    global entries
    global ids
    global topics_scanner_list
    global years_list
    global mode
    print("Scanning for topics...")
    for character in tqdm(entry_names):
        try:
            # get the wikipedia page for the character
            page = wikipedia.page(character)
            # get the text of the page
            page_text = page.content
            # check if the page contains any of the topics in the topics_scanner_list
            if any(
                topic.lower() in page_text.lower() for topic in topics_scanner_list
            ) and any(year.lower() in page_text.lower() for year in years_list):
                entries.append(page_text)
                entry_names.append(character)
                ids.append(str(uuid.uuid4()))
        except:
            print(f"Could not find {character} on wikipedia")


main()
