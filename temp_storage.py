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
master_dict = {} # get the list of keywords from the parent topic page.
# read pages_seen.csv file to populate the pages_seen list
pages_seen = [] # keep track of the pages we have seen already so we don't overtax the wikipedia api
with open('./data/pages_seen.csv', 'r') as f:
    for line in f:
        pages_seen.append(line.strip())
#*###########################################################################################################
#& Functions
#*###########################################################################################################
#& Global Variables:
N = 10 # number of words each child page should have in common with the parent page to be considered.
#*############################################################################################################
#^ Getting the relevant subtopics for a parent topic (e.g. "Machine Learning" for "Artificial Intelligence"). This is done by getting the list of subtopics from the Wikipedia page of the parent topic and then getting the list of keywords (links) from the Wikipedia page of each subtopic. The subtopic is then considered relevant if it has at least N keywords in common with the parent topic.
##############################################################################################################

def filename_create(page_title):
    filename = page_title.replace(" ", "_") # replace spaces with underscores
    filename = filename.replace("/", "_") # replace slashes with underscores
    filename = filename.replace(":", "_") # replace colons with underscores
    filename = filename.replace("?", "_") # replace question marks with underscores
    filename = filename.replace("*", "_") # replace asterisks with underscores
    filename = filename.replace('"', "_") # replace double quotes with underscores
    filename = filename.replace("<", "_") # replace less than signs with underscores
    filename = filename.replace(">", "_") # replace greater than signs with underscores
    filename = filename.replace("|", "_") # replace pipes with underscores
    filename = filename.replace("\\", "_") # replace backslashes with underscores
    filename = filename.replace("(", "_") # replace open parentheses with underscores
    filename = filename.replace(")", "_") # replace close parentheses with underscores
    filename = filename.replace("[", "_") # replace open brackets with underscores
    filename = filename.replace("]", "_") # replace close brackets with underscores
    filename = filename.replace("{", "_") # replace open braces with underscores
    filename = filename.replace("}", "_") # replace close braces with underscores
    filename = filename.replace(",", "_") # replace commas with underscores
    filename = filename.replace(".", "_") # replace periods with underscores
    filename = filename.replace(";", "_") # replace semicolons with underscores
    filename = filename.replace("'", "_") # replace single quotes with underscores
    filename = filename.replace("=", "_") # replace equals signs with underscores
    filename = filename.replace("+", "_") # replace plus signs with underscores
    filename = filename.replace("-", "_") # replace minus signs with underscores
    filename = filename.replace("!", "_") # replace exclamation points with underscore
    filename = filename.replace("@", "_") # replace at signs with underscores
    filename = filename.replace("#", "_") # replace pound signs with underscores
    filename = filename.replace("$", "_") # replace dollar signs with underscores
    filename = filename.replace("%", "_") # replace percent signs with underscores
    filename = filename.replace("^", "_") # replace caret signs with underscores
    filename = filename.replace("&", "_") # replace ampersands with underscores
    filename = filename.replace("~", "_") # replace tildes with underscores
    filename = filename.replace("`", "_") # replace backticks with underscores

    return filename # return the filename


def while_page_exists(page,filename):
    try:
        page_text = page.content # get the content of the page
        # save the page text to a file with the name of the page as the file name in the wikipedia_pages folder
        # to save storage space, we should parse the page_text and remove all extra spaces.
        page_text = re.sub(r"\s+", " ", page_text) # replace all extra spaces with a single space
        with open(f'wikipedia_pages/{filename}.txt', 'w+') as f:
            f.write(page_text)
        print(f'Saved {filename} to file.', end=' ')
        return True
    except:
        return False

@sleep_and_retry
def get_links(topic):
    # get all links from the topic page
    global pages_seen # get the list of topics that have already been seen
    if topic in pages_seen: # if the topic has already been seen, return an empty list
        # get the list of links from the existing file
        filename = filename_create(topic)
        with open(f'wikipedia_pages/{filename}.txt', 'r') as f:
            page_text = f.read()
    try:
        topic_page = wikipedia.page(topic)
        page_name = topic_page.title #* get the title of the page
        filename = filename_create(topic) #& create the filename
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

def divide_into_segments(page_file_content):
    # goal:
    # 1. divide the page into segments based on the pattern '== History ==' where History is the name of a section, and the page_name is the name of the dictionary entry.
    # 2. Save each segment to the dictionary entry for the page_name using the section name as the key.
    # 3. Return the dictionary entry for the page_name.
    # 4. If the page does not have any sections, then save the entire page as the value for the key 'content'.

    # get the list of sections
    sections = re.findall(r"==\s*(.*?)\s*==", page_file_content)
    # get the list of section contents
    section_contents = re.split(r"==\s*(.*?)\s*==", page_file_content)
    # remove the first element of the section_contents list because it is the content before the first section
    section_contents.pop(0)

    # create a dictionary entry for the page_name
    page_dictionary_entry = {}
    # if the page has sections
    if len(sections) > 0:
        # save each section content to the dictionary entry
        for i in range(len(sections)):
            page_dictionary_entry[sections[i]] = section_contents[i]
    # if the page does not have sections
    else:
        # save the entire page as the value for the key 'content'
        page_dictionary_entry["content"] = page_file_content

    return page_dictionary_entry

def add_to_master_dict(subdict):
    # given the results of divide_into_segments, add the subdict to the master dictionary
    # if the page_name is already in the master dictionary, then add the subdict to the existing dictionary entry
    # if the page_name is not in the master dictionary, then add the subdict as a new dictionary entry
    global master_dict
    for page_name in subdict:
        if page_name in master_dict:
            master_dict[page_name].update(subdict[page_name])
        else:
            master_dict[page_name] = subdict[page_name]


def main():
    parent_page = "Exposition Universelle (1889)"
    relevant_subtopics = get_relevant_subtopics(parent_page)
    print(relevant_subtopics)

main()