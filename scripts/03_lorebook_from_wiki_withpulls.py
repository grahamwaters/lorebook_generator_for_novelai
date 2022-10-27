# Imported Libraries
from unicodedata import name
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
import time
import os
import math
from alive_progress import alive_bar
from ratelimit import limits, sleep_and_retry
rest_time = 10 # max number of calls before resting
chunk_size = 10 # number of entries per chunk
warnings.filterwarnings(
    "ignore"
)  # reason we are ignoring the warning is because we are using the wikipedia package to get the content of the articles but we don't mind if we miss a few along the way. As it is right now, the process is designed to be slightly imperfect.

# Global Variables Declaration ------------------------------------------------
# get the list of names from the topics file
nltk.download("stopwords")  # & download stopwords
stop_words = set(stopwords.words("english"))
maxlinksperpage = 30 # how many randomly sampled links to get from each page, to add to the list of keywords
minimum_key_occurrences = 4  # minimum number of times a keyword must appear in the text to be considered a keyword
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

period = 300 # 5 minutes

@sleep_and_retry
#@limits(calls=15, period=period) # 15 calls per 5 minutes
def inner_generator(name,entries,entry_keywords,entry_names,bar):


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
            print(
                "could not find entry for",
                name,
                " trying secondary search result instead",
            )
            for xx in range(1, 5):
                try:
                    entry = wikipedia.search(name)[
                        xx
                    ]  # get the second result from wikipedia, which is usually the most relevant
                    print(f"Looking at the {entry} page")
                    entries.append(entry)
                    entry_names.append(page.title)
                    # entry_keywords.append(entry_keywords)
                    break  # break out of the loop if we find a result
                except:
                    print("could not find summary for", name, " skipping")

def generate_entries_from_list(list_of_names,bar):
    # enter a list of people's names and get a list of entries, from wikipedia
    entries = []
    entry_names = []
    entry_keywords = []
    with alive_bar(len(list_of_names),bar=bar) as bar2:
        for name in list_of_names:
            # pause every 10 iterations to avoid getting blocked by wikipedia (for a random number of seconds)
            # if list_of_names.index(name) % rest_time == 0:
            #     waittime = random.randint(2, 6) # wait between 4 and 15 seconds
            #     bar.text("pausing for " + str(waittime) + " seconds")
            #     time.sleep(waittime)

            bar.text(f"Getting entry for {name}")
            inner_generator(name,entries,entry_keywords,entry_names,bar)
            bar2()
    # generate fake ids for the entries in the format: 642723d1-a4a1-47a3-a63f-d36aee33de1b
    ids = []
    for i in range(len(entries)):
        ids.append(str(uuid.uuid4()))

    print("Entries generated")
    # print(entry_names)
    # print('--------------------------------')
    # print(len(entry_keywords))
    # print('--------------------------------')


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
    # print(f"{entry_name} - entry does not exist")
    return False


def clear_the_lorebook():
    # reset the lorebook to an empty dictionary keeping the same format
    # use the text in the /supporting_files/starter.lorebook file
    with open("./supporting_files/starter.lorebook", "r") as f:
        lore_dict = json.load(f)
    with open("./supporting_files/lorebook_generated.lorebook", "w+") as f:
        json.dump(lore_dict, f, indent=4)
    print("Lorebook cleared")


def clear_all_previously_saved_files():
    # delete all files in the wikipedia_pages folder
    for filename in os.listdir("wikipedia_pages"):
        os.remove(f"wikipedia_pages/{filename}")


def main():
    """
    main function - runs the program, processing the names provided in the characters.csv file and adding them to the lorebook_generated.lorebook file in the supporting_files folder. The function uses the generate_entries_from_list function to generate the entries, and then adds them to the lorebook_generated.lorebook file.
    """
    global context_config
    global minimum_key_occurrences
    global chunk_size # the number of names to process in each chunk
    # open the lorebook_generated.lorebook file
    try:
        with open("./supporting_files/lorebook_generated.lorebook") as f:
            lore_dict = json.load(f)
    except Exception as e:
        print(e)
        print("Error opening lorebook_generated.lorebook file")
        with open("./supporting_files/starter.lorebook") as f:
            lore_dict = json.load(
                f
            )  # if the file doesn't exist, use the starter.lorebook file
    # check those article pages for length (if they are too short, skip them)
    # if they are long enough, and are not already in the list, add them to the list
    list_of_names = pd.read_csv("./data/characters.csv")["Name"].tolist()
    # * we need to be sure that none of the names are "None" or "nan"
    list_of_names = [x for x in list_of_names if str(x) != "nan"]  # remove nan
    list_of_names = [x for x in list_of_names if str(x) != "None"]  # remove None
    list_of_names = [x for x in list_of_names if str(x) != ""]  # remove empty strings
    list_of_names = [x for x in list_of_names if str(x) != " "]  # remove empty strings

    # only keep names in the list of names that are not already in the json file
    print("There are {} names in the list".format(len(list_of_names)))
    print("Checking for names that already exist in the json file")
    list_of_names = [
        x
        for x in list_of_names
        if not check_json_for_entry(x, "./supporting_files/lorebook_generated.lorebook")
    ]

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

    print(f"Generating entries for {len(entry_names)} names")
    print(entry_names[0:5],'...')

    # print(f"Processed {len(entry_names)} names")
    countnans = list_of_names.count("nan")
    print(f"Found {countnans} nan values")
    list_of_names = [x for x in entry_names if str(x) != "nan"]
    print(f"Removed {countnans} nan values")




    # remove any names that are already in the json file
    for entry in range(len(data['entries'])):
        if data['entries'][entry]['displayName'] in list_of_names:
            try:
                list_of_names.remove(data['entries'][entry]['displayName'])
                # and remove the corresponding entry from the entries list
                entries.remove(data['entries'][entry])
                # and remove the corresponding entry from the entry_names list
                entry_names.remove(data['entries'][entry]['displayName'])
                # and remove the corresponding entry from the ids list
                ids.remove(data['entries'][entry]['id'])
                # and remove the corresponding entry from the entry_keywords list
                entry_keywords.remove(data['entries'][entry]['keywords'])
            except Exception as e:
                print(e)
                print(f"Error removing {data['entries'][entry]['displayName']} from the list of names")


    print(f"Removed {len(entry_names) - len(list_of_names)} names that were already in the json file")
    # for each Name
    #todo: chunk this into smaller iteratable chunks and save the results to a file incrementally (will reduce the likelihood of losing all the work if the program crashes or is interrupted. It also will reduce load on the wikipedia API).

    # divide the list of names into as many chunks of 30 as possible and then process each chunk (the final chunk may be smaller than 30).
    # this is to reduce the load on the wikipedia API
    # the chunk size can be changed by changing the chunk_size variable

    number_of_chunks = math.ceil(len(list_of_names) / chunk_size)
    print(f"Processing {number_of_chunks} chunks of {chunk_size} names each")
    for chunk in range(number_of_chunks):
        print(f"Processing chunk {chunk + 1} of {number_of_chunks}")
        # get pages seen from the data directory (if it exists)
        try:
            with open("./data/pages_seen.csv",'r') as f:
                pages_seen = pd.read_csv(f)["Pages"].tolist()
        except Exception as e:
            print(e)
            print("Error opening pages_seen.csv file")
            pages_seen = []

        # convert the list 'pages_seen' to a list of strings
        pages_seen = [str(x).lower() for x in pages_seen]


        with alive_bar(len(list_of_names[chunk * chunk_size : (chunk + 1) * chunk_size]),dual_line=True,title='Chunks Are Processing') as bar:
            for name in list_of_names[chunk * chunk_size : (chunk + 1) * chunk_size]:
                # keys = []  # list of keys for the entry

                if name != "" and name.lower() not in pages_seen:
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
                        bar.text(f"Adding {name} to entries")
                        entries.append(entry)
                        # add this page to pages_seen.csv so that we don't try to get it again
                        pages_seen.append(name)
                        with open("./data/pages_seen.csv", "a+") as f:
                            f.write(f"{name}\n")

                    except Exception as e:
                        print(e)
                        continue


                bar()

            print(f'Resting the wikipedia API for {rest_time} seconds')
            time.sleep(rest_time)
            pd.DataFrame(entry_names).to_pickle('./supporting_files/entry_names.pkl')
            pd.DataFrame(entries).to_pickle('./supporting_files/entries.pkl')



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
        list_of_names, # topics_list
        bar # pass the alive_bar object to the function so that it can be updated
    )

    # remove any keywords from the dictionary that are found in multiple entries, in other words, identify which keys are unique to each entry
    list_of_all_keys = []
    for entry in entry_keywords:
        list_of_all_keys += entry

    print("There are {} keys in the list of all keys".format(len(list_of_all_keys)))

    for entry_keys in entry_keywords:
        keys_row = entry_keys  # get the list of keys for the entry
        print(
            "There are {} keys in the list of keys for this entry".format(len(keys_row))
        )
        keys_row = [x for x in keys_row if x != ""]  # remove empty strings
        keys_row = [
            x for x in keys_row if list_of_all_keys.count(x.lower()) < 2
        ]  # remove keys that are found in more than 1 entries
        # save the entry_keywords list with the new keys
        entry_keywords[entry_keywords.index(entry_keys)] = keys_row
        print(
            "After removing keys that are found in more than 3 entries, there are {} keys in the list of keys for this entry".format(
                len(keys_row)
            )
        )
    # add the words from the entry that are not stopwords and are longer than 3 letters to the list of keywords
    for entry in entries:
        entry_keywords.append(
            [
                word for word in entry.split()
                if word.lower() not in stopwords.words('english')
                and len(word) > 3
            ]
        )

    #!final_checks(entries, entry_names, entry_keywords, lore_dict, list_of_names,ids)

    #!assert(len(entries) == len(entry_names), "The number of entries and entry names must be the same")
    # remove any entries that are already in the lorebook, or are only one word long
    # &entries = [x for x in entries if not check_json_for_entry(x, './supporting_files/lorebook_generated.lorebook')]
    entries = [x for x in entries if len(x.split()) > 1]
    # remove any duplicate entry names
    entry_names = list(dict.fromkeys(entry_names))
    # remove any duplicate entries
    entries = list(dict.fromkeys(entries))
    # entry_names = [x for x in entry_names if not check_json_for_entry(x, './supporting_files/lorebook_generated.lorebook')]
    #!assert(len(entries) == len(entry_names), "after removing existing entries lengths are not the same") # make sure the lengths are the same
    # remove duplicates
    entries = list(dict.fromkeys(entries))



    successful_saves = 0  # count the number of successful saves
    # add the new entries to the lorebook
    with alive_bar(len(entries),dual_line=True,title='Adding Entries to Lorebook') as bar:
        for i in range(len(entries)):
            #!print(f"\nAdding {entry_names[i]} to the lorebook")
            # assert that list_of_names[i] is in the entries[i] string (this is to make sure that the entry is about the correct topic)
            assert(list_of_names[i].lower() in entries[i].lower(), "The entry is not about the correct topic")
            try:
                default_config = {
                    "prefix": "",
                    "suffix": "\n",
                    "tokenBudget": 2048,  # note: this is the number of tokens, not the number of characters
                    "reservedTokens": 0,
                    "budgetPriority": 400,
                    "trimDirection": "trimBottom",
                    "insertionType": "newline",
                    "maximumTrimType": "sentence",
                    "insertionPosition": -1,
                }
                lore_dict["entries"].append(
                    {
                        "displayName": list_of_names[i],
                        "id": ids[i],
                        "keys": entry_keywords[i],
                        "text": entries[i],
                        "lastUpdatedAt": 1666846259188,
                        "searchRange": 10000,
                        "category": "python_generated",
                        "loreBiasGroups": [{"phrases": []}],
                    }
                )
                print(
                    f"Added {entry_names[i]} to the lorebook, with {len(entry_keywords[i])} keywords",
                    end=" ",
                )
                # save the new lorebook
                with open("./supporting_files/lorebook_generated.lorebook", "w") as f:
                    json.dump(lore_dict, f, indent=4)

                print(f" and saved progress...")
                successful_saves += 1
            except Exception as e:
                #print(e)
                continue
            bar()
    print(f"Saved {successful_saves} entries to the lorebook")

    # # for each entry print the number of keys in the keywords list
    # for entry in lore_dict['entries']:
    #     print(f'{entry["displayName"]} has {len(entry["keywords"])} keywords')

    # save the new lorebook dictionary as a json file called lorebook_generated.lorebook
    with open("./supporting_files/lorebook_generated.lorebook", "w+") as f:
        json.dump(lore_dict, f, indent=4)


def final_checks(entries, entry_names, entry_keywords, lore_dict, list_of_names,ids):

    # assert -- make sure the lengths are the same
    assert(len(entries) == len(entry_names), "after removing existing entries lengths are not the same")
    assert(len(entries) == len(entry_keywords), "after removing existing entries lengths are not the same")
    assert(len(entries) == len(ids), "after removing existing entries lengths are not the same")
    assert(len(entry_names) == len(entry_keywords), "after removing existing entries lengths are not the same")
    # check that the name of each entry (i.e. 'Florence Nightingale') is in the first paragraph of the entry's text. If not, then raise an error
    for entry, entry_name in zip(entries, entry_names):
        if entry_name not in entry.split('\n')[0]:
            raise Exception(f"{entry_name} is not in the first paragraph of the entry")



if __name__ == "__main__":

    print("\n\nWelcome to the Lorebook Generator!")
    print("This program will generate a lorebook json file with the pages related to a given topic.")
    print("All subtopics will be saved (article text to the wikipedia_pages directory) and added to the master dictionary.")
    choice = input("\n  Would you like to clear previously generated articles? (y/n) ")
    if choice == "y":
        clear_all_previously_saved_files()

    print("Settings (Current):")
    #todo: maxlinksperpage may not be needed.
    print(f'maxlinksperpage = {maxlinksperpage} - The maximum number of child pages or related links to extract from the pages (and examine).')

    choice = input("Would you like to change settings? (y/n) ")
    if choice == "y":
        maxlinksperpage = int(input("maxlinksperpage = "))
        print(f'maxlinksperpage = {maxlinksperpage} - has been updated.')

    choice = input("Would you like to generate a new lorebook? (y/n): ")

    if choice == "y":

        print(
            "Generating a new lorebook using the template lorebook"
        )  # generate a new lorebook using the template lorebook
        clear_the_lorebook()
    else:
        print("Updating existing lorebook")

    # using all inputs from above generate a new lorebook

    # Basic Checks --
    print(f'Running File Checks...')
    print(f'Check 1. Characters in the list must be unique. (Current):', end='')
    # Check 1. Detect any duplicates in the character list (characters.csv)
    ch_list = pd.read_csv('./data/characters.csv')
    ch_list = ch_list['Name'].tolist() # convert to list
    orig_count = len(ch_list) # get the original count
    ch_list_lower = [x.lower() for x in ch_list] # convert to lowercase
    ch_list_lower = list(dict.fromkeys(ch_list_lower)) # remove duplicates
    # now go through ch_list and remove any characters not in ch_list_lower
    ch_list_upd = [x for x in ch_list if x.lower() in ch_list_lower]
    # save the updated list to the characters.csv file with the header 'Name'
    ch_list_upd = pd.DataFrame(ch_list_upd, columns=['Name'])
    ch_list_upd.to_csv('./data/characters.csv', index=False)
    print(f' {orig_count} characters in the list.')
    if orig_count != len(ch_list_upd):
        print(f'  - {orig_count - len(ch_list_upd)} duplicates removed.')
        print(f'Updated characters.csv file with {len(ch_list_upd)} unique characters.')
    else:
        print(f'\nPassed Check 1.\n')

    main()  # run the main function when the script is run

    print("Done")





# Notes:
# - Add in keys for years and dates, locations, people's names.
# - Add unique words that are used in the entries to the keywords list.
