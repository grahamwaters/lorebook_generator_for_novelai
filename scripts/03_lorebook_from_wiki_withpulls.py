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

warnings.filterwarnings(
    "ignore"
)  # reason we are ignoring the warning is because we are using the wikipedia package to get the content of the articles but we don't mind if we miss a few along the way. As it is right now, the process is designed to be slightly imperfect.

# Global Variables Declaration ------------------------------------------------
# get the list of names from the topics file
nltk.download("stopwords")  # & download stopwords
stop_words = set(stopwords.words("english"))
maxlinksperpage = 30
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
    print(entry_names)

    #!------------------------

    print(f"Processed {len(entry_names)} names")
    countnans = list_of_names.count("nan")
    print(f"Found {countnans} nan values")
    list_of_names = [x for x in entry_names if str(x) != "nan"]
    print(f"Removed {countnans} nan values")
    print(f"Processed {len(entry_names)} names")

    # for each Name
    for name in tqdm(list_of_names):
        keys = []  # list of keys for the entry
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
    for i in range(len(entries)):
        #!print(f"\nAdding {entry_names[i]} to the lorebook")
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

    print(f"Saved {successful_saves} entries to the lorebook")

    # # for each entry print the number of keys in the keywords list
    # for entry in lore_dict['entries']:
    #     print(f'{entry["displayName"]} has {len(entry["keywords"])} keywords')

    # save the new lorebook dictionary as a json file called lorebook_generated.lorebook
    with open("./supporting_files/lorebook_generated.lorebook", "w+") as f:
        json.dump(lore_dict, f, indent=4)


if __name__ == "__main__":
    print("Welcome to the lorebook generator")
    choice = input("Would you like to generate a new lorebook? (y/n): ")

    if choice == "y":

        print(
            "Generating a new lorebook using the template lorebook"
        )  # generate a new lorebook using the template lorebook
        clear_the_lorebook()
    else:
        print("Updating existing lorebook")
    main()  # run the main function when the script is run
    print("Done")
