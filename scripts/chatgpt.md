Graham Waters
I am making a NLP project.
That's great! Natural Language Processing (NLP) is an exciting and growing field of computer science that focuses on helping computers understand and process human languages. It has a wide range of applications, from chatbots and machine translation to sentiment analysis and summarization.




Graham Waters

<div align='center'>
<h1 align="center">

![banner](images/lorebookbanner.png)
</h1>

[![contributions - welcome](https://img.shields.io/badge/contributions-welcome-blue)](/CONTRIBUTING.md "Go to contributions doc") [![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")

![license](https://img.shields.io/github/license/grahamwaters/lorebook_generator_for_novelai)
![ViewCount](https://views.whatilearened.today/views/github/grahamwaters/lorebook_generator_for_novelai.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/grahamwaters/lorebook_generator_for_novelai)
![GitHub repo size](https://img.shields.io/github/repo-size/grahamwaters/lorebook_generator_for_novelai)
![GitHub issues](https://img.shields.io/github/issues/grahamwaters/lorebook_generator_for_novelai)
![GitHub pull requests](https://img.shields.io/github/issues-pr/grahamwaters/lorebook_generator_for_novelai)
</div>


## Table of Contents

- [Table of Contents](#table-of-contents)

- [Introduction](#introduction)

- [Installation](#installation)

- [Usage](#usage)

- [Contributing](#contributing)

- [License](#license)




## Background

This repo is designed to help all of us as authors using NovelAI. It pulls from Wikipedia articles to automatically generate lorebooks for real places or years and pretty much anything you could find on Wikipedia using python's wikipedia library.
The repo contains two different versions: a basic one that generates based on a CSV file, 'characters.csv' and a more advanced version that implements multiple keywords for a more tailored search.

### Basic Comments and Feedback


![](images/main_concept.png)

## How to use this repository

To use this lorebook generator, follow these steps:

- If you are going to contribute or add things to the repository, fork it before you start.
- To start, you need to clone the repo to your local machine. You can do this by running the following command in your terminal:

Note: you will need to replace the url with your forked repos url. If you are not going to contribute, you can use the original url.

```bash
git clone https://github.com/grahamwaters/lorebook_generator_for_novelai
```

Then make sure you navigate into the directory:

```bash
cd lorebook_generator_for_novelai
```

- Next, you need to install the dependencies. You can do this by running the following command:

```bash
pip install -r requirements.txt
```

So, what exactly does this do? Well, it installs all of the dependencies that are required to run the code. You can see the dependencies in the requirements.txt file.

## How does the basic version work?

### Figure A. Basic version (example of keywords)
![example1](images/example1.png)
You can easily tell that in a wikipedia article, the links are usually some sort of entity or concept. In the figure above, you can see that `Queen Victoria`, `Rudyard Kipling` and `Charles Dickens` are all hyperlinks. These will be extracted by our code and used to either reinforce a lorebook to make it more robust or to create a lorebook from scratch.
### Mode 1. Basic Mode - Using a CSV file to generate lorebooks
- Once you have it cloned, populate the `characters.csv` file with your chosen keywords. (You can use the example file as a template.)
- Then run the python script [scripts/03_lorebook_from_wiki_withpulls.py](scripts/03_lorebook_from_wiki_withpulls.py), and it will generate a lorebook for you. This lorebook will be named `lorebook_generated.lorebook` and will be saved in the `supporting_files` folder.

### Mode 2. Subtopics -> to keywords -> to lorebook
If you're feeling adventurous but not super productive, you can provide one topic (wikipedia page) to the [mode_2](./scripts/04_get_relevant_subtopics.py) script and it will generate a list of keywords that are relevant to that topic. Then it will generate a lorebook for you based on those keywords. This is a good way to get a quick lorebook for a topic that you don't know much about. It does currently have limitations in that it will provide WAY more information than you may need for a lorebook. So you may need to do some editing to get it to a place where you're happy with it.



![](images/greatpyramid.png)

The code pulls the wiki page for each character or topic/place in the provided characters file. In the case of the pyramid of Giza, it will scan the text of the article for the significant NNS and NNPS (nouns) and then generate a lorebook with the article's text as the meat of the entry, and each of the unique words will be added in as keywords for NovelAI (which will allow the AI to trigger this entry). The script will also generate a list of the nouns it found in the article, which you can use to add to the characters.csv file if you are interested in building out a more robust contextually dense lorebook.

- Once you have a lorebook created, you can upload the lorebook to NovelAI and use it to add background detail to your stories and characters.
# How to Contribute:

Have an idea?
Make a pull request! Don't be shy!

We are seeking contributors that are skilled at project organization and formatting. If you are interested in helping out, please contact me on Discord: `@its_graham#7425`
Also, feel free to open issues, pull requests, and make suggestions for this project here on GitHub as well. Working together, we could add some more features to the program, like web scraping historical documents or corpora from Project Gutenberg! That would be really informative.

## Included Files -
- [year_specific_lorebook.py](scripts/01_lorebook_from_year.py)
This script generates a lorebook based on a year. It pulls from Wikipedia articles and generates a lorebook based on the year you input. It also generates a list of characters that are mentioned in the article. This is a good way to get a feel for the program and how it works.

- [Lorebook From Articles](scripts/02_lorebook_from_downloaded_wiki_articles.py)
This script generates a lorebook based on a list of keywords. It pulls from Wikipedia articles and generates a lorebook based on the keywords you input. It also generates a list of characters that are mentioned in the article. This is a good way to get a feel for the program and how it works.

- [characters.csv](characters.csv)

This is a CSV file that contains a list of characters that are mentioned in the lorebook. It is generated by the scripts above and will be originally populated by the author to fit their story.


# Areas Currently in Development
- [ ] Working through the notebooks in `notebooks/` to make sure they are up to date with the scripts in `scripts/` and that they are needed.
- [ ] Improving the quality of the generated lorebooks in the following areas:
  - [ ] Parsed Text Extraction Valence Optimization - Currently the text extraction is not perfect. We need to improve the valence of the text extraction to make sure that the text is relevant to the topic being queried. This is a big one.
  - [ ] Integrating sklearn or potentially other libraries to improve the quality of the generated text. (i.e., PyTorch, TensorFlow, etc.)
  - [ ] Identification of instances in the text where the following pattern exists:
    - [ ] `character one` and `character two` are both mentioned within some distance `d` of each other. This is an interesting method of identifying characters that are related to each other. Proximity could be useful in determining how these topics or characters should be considered.


- The code is currently adding a huge number of keys to the lorebook. This is potentially causing problems on the server side of NovelAI. I will reduce the key count to less than fifty and see if that helps.






## Future Development Goals
- [place_specific_lorebook.py](scripts/02_lorebook_from_place.py) - This script will be used to generate lorebooks from a specific place. We will do this by using the Wikipedia library to search for a place and then using the article text as the lorebook entry.

# Notes on the Git Ignore
Make sure to include the following in your `.gitignore` when you fork this repo:
- /wikipedia_pages
- /master_pages
- .lorebook

This will ensure that your literary work is kept confidential and that it is separated from the code improvements you discover along the way.


## Authors

- [@grahamwaters](https://www.github.com/grahamwaters)


## License




[MIT](https://choosealicense.com/licenses/mit/)
The Lorebook Generator is a tool that uses the Python Wikipedia library to automatically generate lorebooks (books containing historical or fictional information) for real places or years and other concepts that can be found on Wikipedia. The repository contains two versions: a basic one that generates a lorebook based on keywords in a CSV file, and an advanced version that allows for multiple keywords to be used for a more tailored search. To use the tool, you will need to clone the repository and install the required dependencies, then run the appropriate Python script. The tool can be useful for authors using the NovelAI platform who want to quickly generate rich and detailed lorebooks for their stories.



Graham Waters
What do you think about my main script?

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


#todo:ticket 0001 - add a function to reduce keywords to a max of 50.
# get the top most unique keywords for the entry as compared to the other entries
def find_unique_keys(keys_dict):
    # the top most unique keywords for the entry as compared to the other entries in the lorebook
    # the keys_dict is a dictionary with all keywords in it.
    # each row is an entry, and each column is a keyword

    # get all the keywords (across all entries) -> keyword_master_list
    # go through each row's keywords and keep them in one of two cases (1) if they occur only once in keyword_master_list or (2) if they occur more than once but the number of keywords currently saved is less than 50 and we have already checked all the keywords in the row for uniqueness.
    # then we go to the next row and repeat the process.

    # code:
    # consolidate all the keywords into one list (from all the entries in keys_dict)
    keyword_master_list = []
    final_keywords = [] # the final list of keywords to return (max 50 in each row)
    for entry in keys_dict:
        keyword_master_list.extend(keys_dict[entry])
    # go through each row's keywords and keep them in one of two cases (1) if they occur only once in keyword_master_list or (2) if they occur more than once but the number of keywords currently saved is less than 50 and we have already checked all the keywords in the row for uniqueness.
    # sort the row's keywords by their frequency (descending)
    for entry in keys_dict:
        sorted_keywords = sorted(keys_dict[entry], key=keys_dict[entry].count, reverse=True) # sort the keywords by their frequency (descending)
        for keyword in sorted_keywords: # go through each keyword in the row
            if keyword_master_list.count(keyword) == 1 or (len(final_keywords) < 50 and keyword not in final_keywords): # if the keyword occurs only once in the master list or if the number of keywords currently saved is less than 50 and we have already checked all the keywords in the row for uniqueness.
                final_keywords.append(keyword) # get the list of names from the topics file




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


        with alive_bar(len(list_of_names[chunk * chunk_size : (chunk + 1) * chunk_size]),dual_line=False,title='Processing') as bar:
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
    # #assert type(topics_list) == list  # make sure it's a list
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

    #!#assert(len(entries) == len(entry_names), "The number of entries and entry names must be the same")
    # remove any entries that are already in the lorebook, or are only one word long
    # &entries = [x for x in entries if not check_json_for_entry(x, './supporting_files/lorebook_generated.lorebook')]
    entries = [x for x in entries if len(x.split()) > 1]
    # remove any duplicate entry names
    entry_names = list(dict.fromkeys(entry_names))
    # remove any duplicate entries
    entries = list(dict.fromkeys(entries))
    # entry_names = [x for x in entry_names if not check_json_for_entry(x, './supporting_files/lorebook_generated.lorebook')]
    #!#assert(len(entries) == len(entry_names), "after removing existing entries lengths are not the same") # make sure the lengths are the same
    # remove duplicates
    entries = list(dict.fromkeys(entries))



    successful_saves = 0  # count the number of successful saves
    # add the new entries to the lorebook
    with alive_bar(len(entries),dual_line=False,title='Adding Entries to Lorebook') as bar:
        for i in range(len(entries)):
            #!print(f"\nAdding {entry_names[i]} to the lorebook")
            # #assert that list_of_names[i] is in the entries[i] string (this is to make sure that the entry is about the correct topic)
            #assert(list_of_names[i].lower() in entries[i].lower(), "The entry is not about the correct topic")
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

                #& Reducing Key Count to at most 50
                entry_keys = entry_keywords[i][:50] # get the list of keys for the entry
                #todo:ticket 0001

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

    # #assert -- make sure the lengths are the same
    #assert(len(entries) == len(entry_names), "after removing existing entries lengths are not the same")
    #assert(len(entries) == len(entry_keywords), "after removing existing entries lengths are not the same")
    #assert(len(entries) == len(ids), "after removing existing entries lengths are not the same")
    #assert(len(entry_names) == len(entry_keywords), "after removing existing entries lengths are not the same")
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
The code you've shared looks like it is a script for generating a lorebook based on keywords. It uses several Python libraries such as Pandas, NLTK, and Wikipedia to extract information from Wikipedia articles and organize it into a lorebook format. It appears to have functions for preprocessing text, finding unique keywords, and examining dates to determine the relevance of articles to each other. It also uses some global variables for settings such as the maximum number of links to get from each page and the minimum number of occurrences for a keyword to be considered relevant. Overall, it looks like a well-structured script with clear comments explaining the different parts of the code.




Graham Waters
Can you explain it to me?
Sure! The code you've shared is a script for generating a lorebook, which is a book containing historical or fictional information. It uses several Python libraries such as Pandas, NLTK, and Wikipedia to extract information from Wikipedia articles and organize it into a lorebook format.

The script starts by importing several libraries that will be used throughout the code. These include Pandas for data manipulation, NLTK for natural language processing, and Wikipedia for accessing and extracting information from Wikipedia articles. The script also defines some global variables such as the maximum number of links to get from each page and the minimum number of occurrences for a keyword to be considered relevant.

The code then has a function called examine_dates which takes in two entries (presumably from a lorebook) and returns a boolean indicating whether the dates in one entry fall within the range of dates in the other entry (with a 10-year error margin). This function uses NLTK's sentence tokenization and named entity recognition to extract dates from the entries and compares them to determine their relevance to each other.

Another function called preprocess takes in a sentence and returns it after performing some basic natural language processing steps such as tokenization and part-of-speech tagging. This is used to help identify relevant keywords and dates in the entries.

The find_unique_keys function takes in a dictionary of keywords and returns the top most unique keywords for a given entry compared to the other entries in the lorebook. It does this by creating a list of all keywords across all entries, then going through each row's keywords and keeping them if they occur only once in the master list or if they occur more than the minimum number of times specified in the global variable minimum_key_occurrences.

Overall, the script appears to be a tool for generating a lorebook from information on Wikipedia. It uses natural language processing and information extraction techniques to extract relevant keywords and dates from Wikipedia articles and organize them into a structured format.




Graham Waters
Can you show me how to simplify each section?
Sure, here is how I would simplify each section of the code:

Imported Libraries
Copy code
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
import time
import os
import math
from alive_progress import alive_bar
from ratelimit import limits, sleep_and_retry

rest_time = 10 # max number of calls before resting
chunk_size = 10 # number of entries per chunk

# ignore warnings related to Wikipedia
warnings.filterwarnings("ignore")

# download NLTK stopwords
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
Global Variables
Copy code
# Global Variables
maxlinksperpage = 30 # max number of links to get from each page
minimum_key_occurrences = 4  # min number of occurrences for a keyword to be considered relevant

# configuration for context insertion
context_config = {
    "prefix": "",
    "suffix": "\n",
    "tokenBudget": 100,
    "reservedTokens": 0,
    "budgetPriority": 400,
    "trimDirection": "trimBottom",
    "insertionType": "newline",
    "maximumTrimType": "sentence",
    "insertionPosition": -1,
}
Function Definitions
Copy code
# preprocess a sentence
def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

# determine if the dates in one entry fall within the range of dates in the other entry
def examine_dates(entry1, entry2):
    # get dates from each entry
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

    # check if the dates in article 1 fall within the range of dates in article 2
    if len(article_one_dates) > 0 and len(article_two_dates) > 0:
        article_one_dates = [int(date) for date in article_one_dates if date.isdigit()]
        article_two_dates = [int(date) for date in article_two_dates if date.isdigit()]
        max_date = max(article



Graham Waters
what improvements would you make?
Here are a few improvements that I would make to the code:

The code uses global variables for settings such as the maximum number of links to get from each page and the minimum number of occurrences for a keyword to be considered relevant. It would be better to pass these values as arguments to the functions that need them instead of using global variables, which can make the code less modular and harder to understand.
Some of the functions, such as examine_dates and find_unique_keys, are quite long and could be broken down into smaller, more focused functions to improve readability and maintainability.
The code could be made more Pythonic by using more concise and idiomatic syntax. For example, instead of using hasattr(chunk, "label") and if chunk.label() == "DATE":, you can use the isinstance built-in function to check the type of chunk and the in keyword to check if "DATE" is in chunk.label().
The code could be improved by adding more comments explaining the purpose and behavior of each function, as well as any important details or assumptions. This would make it easier for other developers to understand the code and use it for their own purposes.
Here is an example of how the code could be refactored to incorporate these improvements:

Copy code
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
import time
import os
import math
from alive_progress import alive_bar
from ratelimit import limits, sleep_and_retry

# ignore warnings related to Wikipedia
warnings.filterwarnings("ignore")

# download NL



Graham Waters
Give me a list of the functions and variables that are not needed or are not used in the code for me to remove.
Return them in a list format.
Here is a list of functions and variables that are not used in the code and can be removed:

The unicodedata library is imported at the top of the code but not used anywhere in the code, so it can be removed.
The uuid library is imported but not used, so it can be removed.
The datetime library is imported but not used, so it can be removed.
The random library is imported but not used, so it can be removed.
The time library is imported but not used, so it can be removed.
The os library is imported but not used, so it can be removed.
The math library is imported but not used, so it can be removed.
The alive_bar function from the alive_progress library is imported but not used, so it can be removed.
The limits and sleep_and_retry functions from the ratelimit library are imported but not used, so they can be removed.
The rest_time and chunk_size variables are defined but not used, so they can be removed.
Here is an example of how the code could be updated to




Graham Waters
How would you have written this code? If your goal was to use keywords to draw from Wikipedia, all the relevant paragraphs? I want to be able to give a function two names or keywords like "Albert Einstein" and "Paris, France" and have a summary of the interactions of those two keyphrases.
Let me clarify what I mean:
"Interactions": co-occurrences of terms.
For a parent page "Paris, France" (feature 1) - look at all children's pages (links on the parent page)
For each child page, if feature 2 ("Albert Einstein") is mentioned, then I want to save the paragraph with the multikey: feature1[child_page_title][feature2] = the section (paragraph) where feature 2 was found.
Here is an example of how I would write this code:

Copy code
import wikipedia

def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [link.title for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    for link in links:
        try:
            # Get the page content
            page2 = wikipedia.page(link)
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs
This code uses the wikipedia library to get the Wikipedia page for the first feature, then extracts the titles of all the links on that page. It then iterates over each of the linked pages, checks if the second feature is mentioned in the page, and if it is, extracts the paragraph containing the second feature and stores it in a dictionary using the link title as the key. If the linked page is a disambiguation page, it is skipped. Finally, the dictionary containing the extracted paragraphs is returned.

Here is an example of how you can use this function:

Copy code
# Extract the paragraphs containing "Albert Einstein" on Wikipedia pages linked from the "Paris, France" page
paragraphs = extract_paragraphs("Paris, France", "Albert Einstein")

# Print the extracted paragraphs
for link, paragraph in paragraphs.items():
    print(f"Paragraph from '{link}' page:")
    print(paragraph)
This will print the paragraphs containing "Albert Einstein" on Wikipedia pages linked from the "Paris, France" page, along with the link titles of the pages where they were found.




Graham Waters
Exception has occurred: PageError
Page id "<built-in method title of str object at 0x7fbde04f8d50>" does not match any pages. Try another id!

During handling of the above exception, another exception occurred:

  File "/Users/grahamwaters/Library/CloudStorage/GoogleDrive-gewaters2@gmail.com/My Drive/lorebook_generator_for_novelai-1/scripts/00_chatGPT_version.py", line 15, in extract_paragraphs
    page2 = wikipedia.page(link)
  File "/Users/grahamwaters/Library/CloudStorage/GoogleDrive-gewaters2@gmail.com/My Drive/lorebook_generator_for_novelai-1/scripts/00_chatGPT_version.py", line 31, in <module>
    paragraphs = extract_paragraphs("Paris, France", "Albert Einstein")
The error message PageError: Page id "<built-in method title of str object at 0x7fbde04f8d50>" does not match any pages. Try another id! indicates that the link.title method returned the string representation of the method itself instead of the title of the link.

To fix this, you can use the str() function to convert the link object to a string before calling the title method. Here is an example of how you can update the code to fix this error:

Copy code
import wikipedia

def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    for link in links:
        try:
            # Get the page content
            page2 = wikipedia.page(link)
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs
This code converts the link object to a string using the str() function before calling the title() method to get the link title. This should fix the PageError and allow the code to extract the paragraphs containing the second feature from the linked pages.




Graham Waters
I am getting an error again for page2 = wikipedia.page(link)

Exception has occurred: PageError
Page id "20th arrondissement of paris" does not match any pages. Try another id!
  File "/Users/grahamwaters/Library/CloudStorage/GoogleDrive-gewaters2@gmail.com/My Drive/lorebook_generator_for_novelai-1/scripts/00_chatGPT_version.py", line 15, in extract_paragraphs
    page2 = wikipedia.page(link)
  File "/Users/grahamwaters/Library/CloudStorage/GoogleDrive-gewaters2@gmail.com/My Drive/lorebook_generator_for_novelai-1/scripts/00_chatGPT_version.py", line 32, in <module>
    paragraphs = extract_paragraphs("Paris, France", "Albert Einstein")

I have an idea.
What if we used switch statements or try blocks here to use variation in how we are getting the page, are there ways to do that?
The error message PageError: Page id "20th arrondissement of paris" does not match any pages. Try another id! indicates that the wikipedia.page(link) method could not find a page with the given title. This can happen if the link title is not exactly the same as the page title on Wikipedia, or if the page with the given title does not exist on Wikipedia.

To fix this, you can use the wikipedia.search() method to search for the page with the given title, and then use the wikipedia.page() method to get the page content. Here is an example of how you can update the code to fix this error:

Copy code
import wikipedia

def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    for link in links:
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # Get the page content
            page2 = wikipedia.page(search_results[0])
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs
This code uses the wikipedia.search() method to search for the page with the given title, and then uses the wikipedia.page() method to get the page content. If no pages were found, the code skips this link. This should fix the PageError and allow the code to extract the paragraphs containing the second feature from the linked pages.




Graham Waters
how can we put a ratelimit on this so we don't get banned?
To avoid getting banned from Wikipedia for making too many requests, you can use the sleep_and_retry and limits decorators from the ratelimit library to limit the rate of requests made to the Wikipedia API. Here is an example of how you can update the code to add a rate limit:

Copy code
import wikipedia
from ratelimit import limits, sleep_and_retry

# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=10, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    for link in links:
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # Get the page content
            page2 = wikipedia.page(search_results[0])
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs
In this code, the @sleep_and_retry and @limits decorators are used to limit the rate of requests made to the Wikipedia API. The @sleep_and_retry decorator is used to retry the request if the rate limit is exceeded, and the @limits decorator is used to specify the rate limit. In this example, the rate limit is set to 10 requests per second. This should prevent the code from getting banned from Wikipedia for making too many requests.




Graham Waters
import wikipedia
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=10, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    for link in tqdm(links):
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # Get the page content
            page2 = wikipedia.page(str(search_results[0]))
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs



# Extract the paragraphs containing "Albert Einstein" on Wikipedia pages linked from the "Paris, France" page
paragraphs = extract_paragraphs("Paris, France", "Albert Einstein")

# Print the extracted paragraphs
for link, paragraph in paragraphs.items():
    print(f"Paragraph from '{link}' page:")
    print(paragraph)
This code adds a rate limit to the extract_paragraphs function, which will limit the number of requests it can make to the Wikipedia API to 10 requests per second. This should help prevent the script from being banned by the Wikipedia servers.

The code also uses the tqdm library to show a progress bar while the function is running, which makes it easier to see the progress of the extraction process. Finally, the code catches and handles wikipedia.exceptions.DisambiguationError exceptions, which are raised when a search for a page returns multiple pages with the same title (i.e. a disambiguation page). In this case, the code simply skips the page and continues to the next one.




Graham Waters
can you please add pbar to this showing a ten character preview of the title of the page in the progress bar?
Here is an updated version of the code that shows a progress bar with a 10-character preview of the title of each page as it is processed by the extract_paragraphs function:

Copy code
import wikipedia
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=10, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    for link in tqdm(links, desc="Extracting paragraphs"):
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # Get the page content
            page2 = wikipedia.page(str(search_results[0]))
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs



# Extract the paragraphs containing "Albert Einstein" on Wikipedia pages linked from the "Paris, France" page
paragraphs = extract_paragraphs("Paris, France", "Albert Einstein")

# Print the extracted paragraphs
for link, paragraph in paragraphs.items():
    print(f"Paragraph from '{link}' page:")
    print(paragraph)
This code uses the desc argument of the tqdm function to specify the description to




Graham Waters
import wikipedia
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=10, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    pbar = tqdm(links)
    for link in pbar:
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # Get the page content
            try:
                page2 = wikipedia.page(str(search_results[0]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[1]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[2]))
                    except wikipedia.exceptions.DisambiguationError:
                        try:
                            page2 = wikipedia.page(str(search_results[3]))
                        except wikipedia.exceptions.DisambiguationError:
                            try:
                                page2 = wikipedia.page(str(search_results[4]))
                            except wikipedia.exceptions.DisambiguationError:
                                continue

            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
                # update the progress bar with the number of extracted paragraphs
                ext_count = len(paragraphs)
                pbar.update(ext_count)

        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs



# Extract the paragraphs containing "Albert Einstein" on Wikipedia pages linked from the "Paris, France" page
paragraphs = extract_paragraphs("Paris, France", "Albert Einstein")

# Print the extracted paragraphs
for link, paragraph in paragraphs.items():
    print(f"Paragraph from '{link}' page:")
    print(paragraph)
You can add a desc parameter to the tqdm call to specify a description for the progress bar. You can use the .set_description() method to update the description of the progress bar as the loop progresses. Here's an example:

Copy code
# Initialize an empty dictionary to store the extracted paragraphs
paragraphs = {}

# Initialize the progress bar with a description
pbar = tqdm(links, desc="Extracting paragraphs")

# For each linked page...
for link in pbar:
    try:
        # Search for the page with the given title
        search_results = wikipedia.search(link)
        # If no pages were found, skip this link
        if not search_results:
            continue
        # Get the page content
        try:
            page2 = wikipedia.page(str(search_results[0]))
        except wikipedia.exceptions.DisambiguationError:
            try:
                page2 = wikipedia.page(str(search_results[1]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[2]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[3]))
                    except wikipedia.exceptions.DisambiguationError:
                        try:
                            page2 = wikipedia.page(str(search_results[4]))
                        except wikipedia.exceptions.DisambiguationError:
                            continue

        # Check if the second feature is mentioned in the page
        if feature2 in page2.content:
            # If the second feature is mentioned, split the page content into paragraphs
            # and store the paragraph containing the second feature in the dictionary
            # using the link title as the key
            paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
            # Update the progress bar description with the title of the page
            pbar.set_description(f"Extracting paragraphs from '{page2.title[:10]}...'")
    except wikipedia.exceptions.DisambiguationError:
        # If the linked page is a disambiguation page, skip it
        continue
This will update the description of the progress bar with the first 10 characters of the title of the page that is being processed. Note that the .set_description() method is only available in tqdm versions greater than 4.43.0. You can check your tqdm version by running pip freeze | grep tqdm. If you have an older version, you can update it by running pip install -U tqdm.




Graham Waters
Exception has occurred: PageError
Page id "20th arrondissement of paris" does not match any pages. Try another id!
  File "/Users/grahamwaters/Library/CloudStorage/GoogleDrive-gewaters2@gmail.com/My Drive/lorebook_generator_for_novelai-1/scripts/00_chatGPT_version.py", line 27, in extract_paragraphs
    page2 = wikipedia.page(str(search_results[0]))
  File "/Users/grahamwaters/Library/CloudStorage/GoogleDrive-gewaters2@gmail.com/My Drive/lorebook_generator_for_novelai-1/scripts/00_chatGPT_version.py", line 63, in <module>
    paragraphs = extract_paragraphs("Paris, France", "Albert Einstein")
It looks like the page2 = wikipedia.page(str(search_results[0])) line is throwing a PageError exception because the page with the given id does not exist. You can try adding a try block around this line of code to catch the exception and continue with the next page in the list. You can also try using a for loop to iterate through the search results and try each one until a page is found. For example:

Copy code
for result in search_results:
    try:
        page2 = wikipedia.page(str(result))
        break
    except wikipedia.exceptions.PageError:
        continue
This will try each search result until a page is found, or until the list of search results is exhausted. If no pages are found, the code will move on to the next linked page.

Additionally, you can add a try block around the wikipedia.search() call to catch the case where no pages are found for the given link title. This will prevent the code from throwing an exception if a page with the given title cannot be found. For example:

Copy code
try:
    search_results = wikipedia.search(link)
    if not search_results:
        continue
except wikipedia.exceptions.PageError:
    continue
This will catch the case where no pages are found for the given link title, and continue with the next linked page.

I hope this helps! Let me know if you have any further questions.




Graham Waters
import wikipedia
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=10, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    pbar = tqdm(links)
    for link in pbar:
        pbar.set_description(f"Scanning '{link}...'")
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # Get the page content
            try:
                page2 = wikipedia.page(str(search_results[0]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[1]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[2]))
                    except wikipedia.exceptions.DisambiguationError:
                        try:
                            page2 = wikipedia.page(str(search_results[3]))
                        except wikipedia.exceptions.DisambiguationError:
                            try:
                                page2 = wikipedia.page(str(search_results[4]))
                            except Exception as e:
                                print(f'Error: {e}')
                                continue
            except wikipedia.exceptions.PageError:
                continue
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
                # update the progress bar with the number of extracted paragraphs
                # ext_count = len(paragraphs)
                pbar.set_description(f"Extracting paragraphs from '{page2.title[:10]}...'")

        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs



# Extract the paragraphs containing "Albert Einstein" on Wikipedia pages linked from the "Paris, France" page
paragraphs = extract_paragraphs("Paris, France", "Nikola Tesla")

# Print the extracted paragraphs
for link, paragraph in paragraphs.items():
    print(f"Paragraph from '{link}' page:")
    print(paragraph)
Here is a version of the code that uses a try / except block to handle the DisambiguationError and PageError exceptions that can be thrown by the wikipedia module. Additionally, the tqdm library is used to show a progress bar during the extraction process, which is also updated with a ten character preview of the title of the page being scanned.

Copy code
import wikipedia
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=10, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    pbar = tqdm(links)
    for link in pbar:
        pbar.set_description(f"Scanning '{link}...'")
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # Get the page content
            try:
                page2 = wikipedia.page(str(search_results[0]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[1]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[2]))
                    except wikipedia.exceptions.DisambiguationError:
                        try:
                            page2 = wikipedia.page(str(search_results[3]))
                        except wikipedia.exceptions.DisambiguationError:
                            try:
                                page2 = wikipedia.page(str(search_results[4]))
                            except Exception as e:
                                print(f'Error: {e}')
                                continue
            except wikipedia.exceptions.PageError:
                continue
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
                # update the progress bar with the number of extracted paragraphs
                # ext_count = len(paragraphs)
                pbar.set_description(f"Extracting paragraphs from '{page2.title[:10]}...'")

        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs



# Extract the paragraphs containing "Albert Einstein"



Graham Waters
what should I add to save these paragraphs to a pandas dataframe and then a csv file? Use step-by-step and pythonic code. Only show me the new lines.
To save the extracted paragraphs to a Pandas DataFrame and then to a CSV file, you can do the following:

Import the Pandas library at the beginning of the script:

Copy code
import pandas as pd
After extracting the paragraphs, create a Pandas DataFrame from the paragraphs dictionary using the from_dict() method. You can also specify the column names for the dataframe as "link" and "paragraph":

Copy code
df = pd.DataFrame.from_dict(paragraphs, orient='index', columns=["link", "paragraph"])
Use the to_csv() method to save the dataframe to a CSV file. For example, you can specify the file path and name as "extracted_paragraphs.csv":

Copy code
df.to_csv("extracted_paragraphs.csv")
You can also specify additional options such as the delimiter and quoting character for the CSV file using the sep and quotechar arguments, respectively. For example:

Copy code
df.to_csv("extracted_paragraphs.csv", sep=",", quotechar='"')
This will create a CSV file with the extracted paragraphs, where each row contains the link title and the corresponding paragraph. The link and paragraph values will be separated by a comma and quoted using double quotes.

Here is the complete code with the above steps implemented:

Copy code
import wikipedia
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm
import pandas as pd

# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=10, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    pbar = tqdm(links)
    for link in pbar:
        pbar.set_description(f"Scanning '{link}...'")
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # Get the page content
            try:
                page2 = wikipedia.page(str(search_results[0]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[1]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[2]))
                    except wikipedia.exceptions.DisambiguationError:
                        try:
                            page2 = wikipedia.page(str(search_results[3]))
                        except wikipedia.exceptions.DisambiguationError:
                            try:



Graham Waters
what issues are there in the code?

import wikipedia
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm
import pandas as pd


# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=10, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    paragraphs = {}
    # For each linked page...
    pbar = tqdm(links)
    for link in pbar:
        pbar.set_description(f"Scanning '{link}...'")
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # Get the page content
            try:
                page2 = wikipedia.page(str(search_results[0]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[1]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[2]))
                    except wikipedia.exceptions.DisambiguationError:
                        try:
                            page2 = wikipedia.page(str(search_results[3]))
                        except wikipedia.exceptions.DisambiguationError:
                            try:
                                page2 = wikipedia.page(str(search_results[4]))
                            except Exception as e:
                                print(f'Error: {e}')
                                continue
            except wikipedia.exceptions.PageError:
                continue
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
                # update the progress bar with the number of extracted paragraphs
                # ext_count = len(paragraphs)
                print(f'Found {len(paragraphs)} paragraphs in {page2.title} that mention {feature2}')
                pbar.set_description(f"Extracting paragraphs from '{page2.title[:10]}...'")

        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs

# Extract the paragraphs from the parent page of the first feature, that mention the second feature.
# The first feature is the parent page of the second feature.
paragraphs = extract_paragraphs("Queen Victoria", "Nikola Tesla")

# save the extracted paragraphs to a csv file
df = pd.DataFrame.from_dict(paragraphs, orient='index', columns=["link", "paragraph"])
df.to_csv("../data/ai_identified_paragraphs.csv", index=False)

# Print the extracted paragraphs
for link, paragraph in paragraphs.items():
    print(f"Paragraph from '{link}' page:")
    print(paragraph)
There are several issues with the code:

In the extract_paragraphs function, the paragraphs dictionary is initialized with keys as the titles of the linked pages and values as None. However, when extracting paragraphs from the linked pages, you are trying to store the paragraph in the paragraphs dictionary using the title of the linked page as the key, but since the dictionary already has keys with the same names, the paragraph will not be added to the dictionary. To fix this, you can simply initialize the paragraphs dictionary with empty values for each key.
In the same function, you are trying to update the progress bar with the number of extracted paragraphs, but you are not updating the value of the ext_count variable, which is used to update the progress bar. As a result, the progress bar will not be updated.
In the same function, you are using the continue statement to skip a linked page if it is a disambiguation page. However, you are using this continue statement in the try-except block where you are trying to get the content of the linked page, so even if the linked page is a disambiguation page, the code will still try to access the page content, which will result in an error. To fix this, you can move the continue statement to the except block where you are catching the DisambiguationError exception.
In the try-except block where you are trying to get the content of the linked page, you are catching the DisambiguationError exception and trying to access the content of one of the pages listed on the disambiguation page. However, you are not checking if the disambiguation page actually lists any pages, so if the disambiguation page doesn't have any listed pages, your code will try to access an index that doesn't exist in the list of search results, which will result in an error. To fix this, you can check the length of the search_results list before trying to access its elements.
In the same try-except block, you are using



Graham Waters
            # check length of search results before trying to access them
            if len(search_results) < 5:
                continue
would this fix issue: 4 ? I am not sure what to put here.
Yes, this would fix the issue where the code tries to access an element in the search_results list that does not exist. In the try block, you can check the length of search_results and only try to access elements that are within the bounds of the list. Here is an example of how you can do this:

Copy code
# Check if there are at least 5 search results
if len(search_results) >= 5:
    # Get the page content
    try:
        page2 = wikipedia.page(str(search_results[0]))
    except wikipedia.exceptions.DisambiguationError:
        try:
            page2 = wikipedia.page(str(search_results[1]))
        except wikipedia.exceptions.DisambiguationError:
            try:
                page2 = wikipedia.page(str(search_results[2]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[3]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[4]))
                    except Exception as e:
                        print(f'Error: {e}')
                        continue
else:
    # If there are less than 5 search results, skip this link
    continue
This code first checks if there are at least 5 search results. If there are, it tries to get the page content for the first 5 search results, just like before. If there are less than 5 search results, it skips this link and goes on to the next one. This way, it won't try to access an element in the search_results list that does not exist, which




Graham Waters
import wikipedia
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm
import pandas as pd


# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=10, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    # paragraphs = {}

    # In the extract_paragraphs function, the paragraphs dictionary is initialized with keys as the titles of the linked pages and values as None. However, when extracting paragraphs from the linked pages, you are trying to store the paragraph in the paragraphs dictionary using the title of the linked page as the key, but since the dictionary already has keys with the same names, the paragraph will not be added to the dictionary. To fix this, you can simply initialize the paragraphs dictionary with empty values for each key.
    # fix
    paragraphs = {link: None for link in links}


    # For each linked page...
    pbar = tqdm(links)
    for link in pbar:
        pbar.set_description(f"Scanning '{link}...'")
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # check length of search results before trying to access them
            if len(search_results) < 5: # if less than 5 results, skip this link in the loop
                continue # skip this link
            # Get the page content
            try:
                page2 = wikipedia.page(str(search_results[0]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[1]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[2]))
                    except wikipedia.exceptions.DisambiguationError:
                        try:
                            page2 = wikipedia.page(str(search_results[3]))
                        except wikipedia.exceptions.DisambiguationError:
                            try:
                                page2 = wikipedia.page(str(search_results[4]))
                            except Exception as e:
                                continue
            except wikipedia.exceptions.PageError:
                continue
            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
                print(f'Found {len(paragraphs)} paragraphs in {page2.title} that mention {feature2}')
                pbar.set_description(f"Extracting paragraphs from '{page2.title[:10]}...'")

        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs

# Extract the paragraphs from the parent page of the first feature, that mention the second feature.
# The first feature is the parent page of the second feature.
paragraphs = extract_paragraphs("Queen Victoria", "Nikola Tesla")

# save the extracted paragraphs to a csv file
df = pd.DataFrame.from_dict(paragraphs, orient='index', columns=["link", "paragraph"])
df.to_csv("../data/ai_identified_paragraphs.csv", index=False)

# Print the extracted paragraphs
for link, paragraph in paragraphs.items():
    print(f"Paragraph from '{link}' page:")
    print(paragraph)
In the extract_paragraphs function, the paragraphs dictionary is initialized with keys as the titles of the linked pages and values as None. However, when extracting paragraphs from the linked pages, you are trying to store the paragraph in the paragraphs dictionary using the title of the linked page as the key, but since the dictionary already has keys with the same names, the paragraph will not be added to the dictionary. To fix this, you can simply initialize the paragraphs dictionary with empty values for each key.

Another issue is that in the try-except block where you are trying to get the page content, you are catching the DisambiguationError and trying to get the page content from the first few search results. However, if the search result is not a Wikipedia page but a disambiguation page, trying to get the page content of the disambiguation page will raise a DisambiguationError. This can be fixed by using the PageError instead of the DisambiguationError.




Graham Waters
like this?

    paragraphs = {link: '' for link in links}
Yes, that would work. Instead of initializing the dictionary with empty values, you could also initialize it with empty strings. This would make sure that the dictionary keys are created, and you can then store the extracted paragraphs in the dictionary using these keys.

Copy code
paragraphs = {link: '' for link in links}

# For each linked page...
pbar = tqdm(links)
for link in pbar:
    pbar.set_description(f"Scanning '{link}...'")
    try:
        # Search for the page with the given title
        search_results = wikipedia.search(link)
        # If no pages were found, skip this link
        if not search_results:
            continue
        # check length of search results before trying to access them
        if len(search_results) < 5: # if less than 5 results, skip this link in the loop
            continue # skip this link
        # Get the page content
        try:
            page2 = wikipedia.page(str(search_results[0]))
        except wikipedia.exceptions.DisambiguationError:
            try:
                page2 = wikipedia.page(str(search_results[1]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[2]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[3]))
                    except wikipedia.



Graham Waters
how can I check if the page is a person wiki page, or a place etc?
To check if a page is a person or place page in Wikipedia, you can use the page.categories property of the wikipedia.page object. This property returns a list of categories that the page belongs to. You can check if the page belongs to any of the categories that are typically associated with person pages, such as "Category:People from", "Category:American people", etc., or any of the categories associated with place pages, such as "Category:Populated places", "Category:Capitals in Europe", etc.

Here is an example of how you can check if a page is a person or place page:

Copy code
import wikipedia

# Get the Wikipedia page for "Albert Einstein"
page = wikipedia.page("Albert Einstein")

# Check if the page belongs to any of the categories that are typically associated with person pages
person_categories = ["Category:People from", "Category:American people", "Category:German people", "Category:Swiss people"]
if any(category in person_categories for category in page.categories):
    print("The page is a person page.")
else:
    print("The page is not a person page.")

# Check if the page belongs to any of the categories that are typically associated with place pages
place_categories = ["Category:Populated places", "Category:Capitals in Europe", "Category:Cities in Germany"]
if any(category in place_categories for category in page



Graham Waters
but there are so many categories on wikipedia...
The Wikipedia API does not provide a straightforward way to check the category of a page. You can, however, use the page.categories attribute of the WikipediaPage object to get a list of categories that the page belongs to. This list can be used to check if the page belongs to a particular category or not.

For example, to check if a page belongs to the category of "People", you can do the following:

Copy code
# Check if the page belongs to the 'People' category
if "People" in page.categories:
    # The page belongs to the 'People' category
    # Do something
else:
    # The page does not belong to the 'People' category
    # Do something else
You can use the page.categories attribute to check if the page belongs to a particular category and take appropriate action based on the result. Note that the page.categories attribute is a list of categories, so you will need to use in operator to check if a particular category is present in the list.




Graham Waters
okay, so I could use
if "Place" in page.categories?
if "People" in page.categories
Yes, that is one way to check if a page belongs to a particular category on Wikipedia. You can use the page.categories property to access the categories that the page belongs to, and then check if the page belongs to a particular category by using the in keyword to check if the category name is in the list of categories.

For example:

Copy code
page = wikipedia.page("Paris, France")
if "Place" in page.categories:
    print(f"The page '{page.title}' belongs to the 'Place' category on Wikipedia.")
However, keep in mind that the names of categories on Wikipedia are case-sensitive, so you need to make sure to match the case of the category names correctly.

Alternatively, you can use the page.section() method to access the sections of the page, and then check if the page belongs to a particular category by looking for a section with the name of the category. For example:

Copy code
page = wikipedia.page("Paris, France")
sections = page.sections
if "Place" in sections:
    print(f"The page '{page.title}' belongs to the 'Place' category on Wikipedia.")
This method is more robust since it is not affected by the case of the category names. However, it is also more expensive since it involves loading the sections of the page, which can be slow for large pages.




Graham Waters
so if page.categories contains 'births' and 'people' in any of the categories then it's likely a person. write an if statement to check for this please.
Note: "'17th-century English people'" is a cat. that contains "people" so it sets the people_bool_flag to True.
Note: "1665 births" contains "birth" which sets "births" flag to True.
so categories may "contain" the words within the string of the category name.
Here is an example if statement you can use to check if a Wikipedia page is about a person:

Copy code
if "People" in page.categories or "births" in page.categories:
    people_bool_flag = True
This if statement checks if the page has a category that contains the word "People" or "births". If either of these words is present in any of the page's categories, the people_bool_flag is set to True.

You can use this flag to determine if the page is likely about a person, and take any necessary actions based on that. For example, you can filter out pages that are not about people and only extract paragraphs from pages that are likely about people.




Graham Waters
it needs to be like a list comprehension. [r'people|People' in category_string for category_string in page.categories] or something like that.
Yes, you can use a list comprehension to check if the categories of a page contain the words "people" or "People". Here is an example:

Copy code
# Get the categories of a page
categories = page.categories

# Set the "people" and "births" flags to False
people_flag = False
births_flag = False

# Use a list comprehension to check if the categories contain the words "people" or "People"
people_flag = any(["people" in category.lower() for category in categories])

# Use a list comprehension to check if the categories contain the word "births"
births_flag = any(["births" in category.lower() for category in categories])

# If the "people" and "births" flags are True, the page is likely a person page
if people_flag and births_flag:
    # Do something...
The list comprehension in this example checks if any of the categories of a page contain the words "people" or "People", and sets the "people_flag" to True if any of the categories contain these words. It also checks if any of the categories contain the word "births", and sets the "births_flag" to True if any of the categories contain this word. Finally, it checks if both the "people_flag" and "births_flag" are True, indicating that the page is likely a person page.

You can modify this code to check for other keywords in the categories of a page, or to perform different actions depending on whether the page is likely a person page or not.




Graham Waters
make this a one-liner with regex
To check if a page is about a person, you can use a regular expression to match the page categories against a pattern that looks for the words "people" or "births". The regular expression should be case-insensitive to match both "people" and "People". You can use the search method of the re module to match the pattern against each category string in the page.categories list, and use a list comprehension to return a list of booleans, indicating whether the pattern was found in each category string.

To check if a page is about a person, you can use the following one-liner:

Copy code
is_person = any([re.search(r'people|births', category, re.IGNORECASE) for category in page.categories])
Here, the regular expression r'people|births' matches any category string that contains either "people" or "births". The re.IGNORECASE flag makes the search case-insensitive. The search method returns a Match object if the pattern is found in the category string, and None if the pattern is not found. The list comprehension returns a list of Match objects, which are "truthy" values, or None values if the pattern is not found in the category string. The any function returns True if any of the elements in the list are "truthy", and False if all elements are "falsy". Therefore, the is_person variable will be True if the page is about a person, and False if the page is not about a person.




Graham Waters
SyntaxError('invalid syntax', ('<string>', 1, 11, "is_person = any([re.search(r'people|births', category, re.IGNORECASE) for category in page.categories])"))
You can use the any function along with a regular expression to check if any of the categories in page.categories match the regular expression r'people|births' (ignoring the case of the characters). Here's an example:

Copy code
import re

# Create a regular expression that matches the words "people" or "births" (ignoring the case of the characters)
pattern = re.compile(r'people|births', re.IGNORECASE)

# Use the any function to check if any of the categories in page.categories match the regular expression
is_person = any(pattern.search(category) for category in page.categories)
In the code above, the is_person variable will be True if any of the categories in page.categories match the regular expression, and False otherwise. You can use this variable to check if the page is likely to be about a person or not.

Note: If you want to use this code, you'll need to import the re module at the beginning of your script.




Graham Waters
import wikipedia
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm
import pandas as pd
import re
# Create a regular expression that matches the words "people" or "births" (ignoring the case of the characters)
pattern = re.compile(r'people|births', re.IGNORECASE)
events_pattern = re.compile(r'events', re.IGNORECASE)
locations_pattern = re.compile(r'locations|Coordinates|location|city|place', re.IGNORECASE)
# Set the rate limit to 10 requests per second
@sleep_and_retry
@limits(calls=20, period=1)
def extract_paragraphs(feature1, feature2):
    # Get the Wikipedia page for the first feature
    page1 = wikipedia.page(feature1)
    # Get the titles of all the links on the page
    links = [str(link).title() for link in page1.links]

    # Initialize an empty dictionary to store the extracted paragraphs
    # paragraphs = {}

    # In the extract_paragraphs function, the paragraphs dictionary is initialized with keys as the titles of the linked pages and values as None. However, when extracting paragraphs from the linked pages, you are trying to store the paragraph in the paragraphs dictionary using the title of the linked page as the key, but since the dictionary already has keys with the same names, the paragraph will not be added to the dictionary. To fix this, you can simply initialize the paragraphs dictionary with empty values for each key.
    # fix
    paragraphs = {link: '' for link in links}


    # For each linked page...
    pbar = tqdm(links)
    for link in pbar:
        pbar.set_description(f"Scanning '{link}...'")
        try:
            # Search for the page with the given title
            search_results = wikipedia.search(link)
            # If no pages were found, skip this link
            if not search_results:
                continue
            # check length of search results before trying to access them
            if len(search_results) < 5: # if less than 5 results, skip this link in the loop
                continue # skip this link
            # Get the page content
            try:
                page2 = wikipedia.page(str(search_results[0]))
            except wikipedia.exceptions.DisambiguationError:
                try:
                    page2 = wikipedia.page(str(search_results[1]))
                except wikipedia.exceptions.DisambiguationError:
                    try:
                        page2 = wikipedia.page(str(search_results[2]))
                    except wikipedia.exceptions.DisambiguationError:
                        try:
                            page2 = wikipedia.page(str(search_results[3]))
                        except wikipedia.exceptions.DisambiguationError:
                            try:
                                page2 = wikipedia.page(str(search_results[4]))
                            except Exception as e:
                                continue
            except wikipedia.exceptions.PageError:
                continue
            # check if is person


            # Use the any function to check if any of the categories in page.categories match the regular expression
            is_person = any(pattern.search(category) for category in page2.categories)
            is_event = any(events_pattern.search(category) for category in page2.categories)
            is_location = any(locations_pattern.search(category) for category in page2.categories)
            # If the page is a person, print the page title
            if is_person:
                print(f'person found: {page2.title}')
            if is_event:
                print(f'event found: {page2.title}')
            if is_location:
                print(f'location found: {page2.title}')

            # Check if the second feature is mentioned in the page
            if feature2 in page2.content:
                # If the second feature is mentioned, split the page content into paragraphs
                # and store the paragraph containing the second feature in the dictionary
                # using the link title as the key
                paragraphs[link] = next(p for p in page2.content.split("\n\n") if feature2 in p)
                print(f'Found {len(paragraphs)} paragraphs in {page2.title} that mention {feature2}')
                pbar.set_description(f"Extracting paragraphs from '{page2.title[:10]}...'")

        except wikipedia.exceptions.DisambiguationError:
            # If the linked page is a disambiguation page, skip it
            continue

    # Return the dictionary containing the extracted paragraphs
    return paragraphs

# Extract the paragraphs from the parent page of the first feature, that mention the second feature.
# The first feature is the parent page of the second feature.
paragraphs = extract_paragraphs("Queen Victoria", "Nikola Tesla")

# save the extracted paragraphs to a csv file
df = pd.DataFrame.from_dict(paragraphs, orient='index', columns=["link", "paragraph"])
df.to_csv("../data/ai_identified_paragraphs.csv", index=False)

# Print the extracted paragraphs
for link, paragraph in paragraphs.items():
    print(f"Paragraph from '{link}' page:")
    print(paragraph)
To fix this issue, you can use the get method of a dictionary to retrieve the value associated with a key. If the key is not present in the dictionary, the get method will return a default value that you specify.

Here is an example:

Copy code
# Create a dictionary with some keys and values
d = {'key1': 'value1', 'key2': 'value2'}

# Print the value associated with 'key1'
print(d['key1']) # Output: 'value1'

# Print the value associated with 'key3' (which does not exist in the dictionary)
# If the key does not exist, return the default value 'default_value'
print(d.get('key3', 'default_value')) # Output: 'default_value'
To fix the code in the extract_paragraphs function, you can use the get method to retrieve the paragraph from the paragraphs dictionary. If the paragraph does not exist, the get method will return an empty string.

Here is an example:

Copy code
# Initialize the paragraphs dictionary with some keys and empty values
paragraphs = {'key1': '', 'key2': ''}

# Print the value associated with 'key1'
print(paragraphs['key1']) # Output: ''

# Print the value associated with 'key3' (which does not exist in the dictionary)
# If the key does not exist, return the default value ''
print(paragraphs.get('key3', '')) # Output: ''
To apply this to the code in the extract_paragraphs function, you can replace this line:

Copy code
paragraph = paragraphs[link]
with this line:

Copy code
paragraph = paragraphs.get(link, '')
This will fix the error and allow the code to continue executing even if the paragraphs dictionary does not contain the key link.



Try again

Free Research Preview: ChatGPT is optimized for dialogue. Our goal is to make AI systems more natural to interact with, and your feedback will help us improve our systems and make them safer.
Reset Thread
Light Mode
OpenAI Discord
Updates & FAQ
Log out
