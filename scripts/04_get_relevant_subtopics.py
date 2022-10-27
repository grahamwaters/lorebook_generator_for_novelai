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
import ratelimit
from ratelimit import limits, sleep_and_retry

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

#*###########################################################################################################
#& Functions
#*###########################################################################################################
#& Global Variables:
N = 10 # number of words each child page should have in common with the parent page to be considered.
#*############################################################################################################
#^ Getting the relevant subtopics for a parent topic (e.g. "Machine Learning" for "Artificial Intelligence"). This is done by getting the list of subtopics from the Wikipedia page of the parent topic and then getting the list of keywords (links) from the Wikipedia page of each subtopic. The subtopic is then considered relevant if it has at least N keywords in common with the parent topic.
##############################################################################################################

def while_page_exists(page):
    try:
        page_text = page.content # get the content of the page
        # save the page text to a file with the name of the page as the file name in the wikipedia_pages folder
        with open(f'wikipedia_pages/{page.title}.txt', 'w+') as f:
            f.write(page_text)
        print(f'Saved {page.title} to file.')
        return True
    except:
        return False

@sleep_and_retry
def get_links(topic):
    # get all links from the topic page
    try:
        topic_page = wikipedia.page(topic)
        topic_links = topic_page.links
        #? While the page exists save the page text to a file with the name of the page as the file name in the wikipedia_pages folder
        while_page_exists(topic_page)
    except:
        topic_links = []

    return topic_links

def get_relevant_subtopics(parent_topic):
    # get the list of subtopics from the parent topic page.
    # get all links from the parent topic page

    # make sure that the topic page will show up in the search results
    parent_topic_links = get_links(parent_topic)
    #note: could use a for loop above until len(parent_topic_links) > 0

    # get the list of subtopics from the parent topic page.
    subtopics = []
    for link in tqdm(parent_topic_links):
        if ":" not in link:
            subtopics.append(link)

    # get the list of keywords from the parent topic page.
    parent_topic_keywords = get_links(parent_topic)

    # get the list of keywords from each subtopic page.
    subtopics_keywords = {}
    for subtopic in tqdm(subtopics):
        print(f'Getting keywords for {subtopic}...', end=' ')
        subtopics_keywords[subtopic] = get_links(subtopic)
        print(f'Found {len(subtopics_keywords[subtopic])}')

    # get the list of relevant subtopics
    relevant_subtopics = []
    for subtopic in subtopics_keywords:
        # get the number of keywords in common between the parent topic and the subtopic
        common_keywords = set(parent_topic_keywords).intersection(
            set(subtopics_keywords[subtopic])
        )
        if len(common_keywords) >= N:
            relevant_subtopics.append(subtopic)

    return relevant_subtopics

def main():
    parent_page = "Exposition Universelle (1889)"
    relevant_subtopics = get_relevant_subtopics(parent_page)
    print(relevant_subtopics)

main()