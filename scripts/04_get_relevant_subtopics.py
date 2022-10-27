# Imported Libraries
import re
import nltk
from nltk.corpus import stopwords
import wikipedia
from tqdm import tqdm
import warnings
from ratelimit import sleep_and_retry
import os

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
# save the keys from the keys_dict.csv file to a dict: keys_dict
keys_dict = {}
with open("./data/keys_dict.csv", "r") as f:
    for line in f:
        line = line.strip()
        line = line.split(",")
        keys_dict[line[0]] = line[1]

#*###########################################################################################################
#& Functions
#*###########################################################################################################
#& Global Variables:
N = 10 # number of words each child page should have in common with the parent page to be considered.
#*############################################################################################################
#^ Getting the relevant subtopics for a parent topic (e.g. "Machine Learning" for "Artificial Intelligence"). This is done by getting the list of subtopics from the Wikipedia page of the parent topic and then getting the list of keywords (links) from the Wikipedia page of each subtopic. The subtopic is then considered relevant if it has at least N keywords in common with the parent topic.
##############################################################################################################
def preprocess_sentence(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def filename_create(page_title):
    filename = page_title.replace(" ", "_") # replace spaces with underscores
    filename = filename.replace("/", "_") # replace slashes with underscores
    filename = filename.replace(":", "_") # replace colons with underscores
    filename = filename.replace("?", "_") # replace question marks with underscores
    filename = filename.replace("*", "_") # replace asterisks with underscores
    filename = filename.replace('"', "") # replace double quotes with underscores
    filename = filename.replace("'", "") # replace single quotes with underscores
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
    filename = filename.replace("__","_") # replace double underscores with single underscores

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

def topic_check_pos_type(topic):
    # Using NLTK, determine what POS the topic word is and return True if it is a noun, False if it is not
    # if the topic word is a noun, then we can use it as a keyword to search for subtopics
    # if the topic word is not a noun, then we cannot use it as a keyword to search for subtopics
    topic_processed = preprocess_sentence(topic) # preprocess the topic word

    # Noun-phrase chunking to identify entities in the topic
    pattern = r"NP: {<DT|PP\$>?<JJ>*<NN>}"   # chunk determiner/possessive, adjectives and noun
    cp = nltk.RegexpParser(pattern) # create the chunk parser
    cs = cp.parse(topic_processed) # parse the topic
    # if the entity is a person, country, organization, or historical event, then keep going otherwise return False
    if cs[0][1] == 'NNP' or cs[0][1] == 'NNPS' or cs[0][1] == 'NN' or cs[0][1] == 'NNS':
        return True
    else:
        return False

    # # get the POS of the topic word
    # topic_pos = nltk.pos_tag([topic])[0][1]

    # # if the topic word is a noun, then return True
    # if topic_pos[0] == "N": # if the first letter of the POS is N, then it is a noun
    #     return True
    # else:
    #     return False # if the topic word is not a noun, then return False

def book_keeper_bot(topic):
    # this function will check if the topic has already been saved to the wikipedia_pages folder
    # if it has, then it will return True
    # if it has not, then it will return False
    filename = filename_create(topic) # create the filename
    if os.path.exists(f'./wikipedia_keys/{filename}.csv'): # if the file exists, then return True
        return True
    else:
        return False


#check if the topic has a file in the wikipedia_pages or wikipedia_keys folder
# def book_keeper(topic):
#     # this function will check if the topic has already been saved to the wikipedia_pages folder
#     # if it has, then it will return True
#     # if it has not, then it will return False
#     filename = filename_create(topic) # create the filename
#     if os.path.exists(f'./wikipedia_pages/{filename}.csv'): # if the file exists, then return True
#         return True
#     else:
#         return False


@sleep_and_retry # retry if there is an error, wait 5 seconds between retries
def get_links(topic):

    # If the topic has already been saved to the wikipedia_pages folder, then skip it
    status = book_keeper_bot(topic) # check if the topic has already been saved to the wikipedia_pages folder
    #//status = book_keeper(topic) # check if the topic has already been saved to the wikipedia_pages folder
    if status == True: # if the topic has already been saved to the wikipedia_pages folder, then skip it
        print(f'{topic} has already been saved to the wikipedia_pages folder.',end=' -> ')
        # open the file and get the links
        filename = filename_create(topic) # create the filename
        with open(f'./wikipedia_keys/{filename}.csv', 'r') as f:
            links = f.read().splitlines() # read the file and split the lines into a list
        #links.replace('\n', ',') # replace the new line characters with commas
        #links = links.split(',') # split the links into a list
        print(f' loaded {len(links)} links from file.')
        return links # return the links
    # get all links from the topic page
    try:
        # filename
        #& using topic_check_pos_type(topic) to check if the topic word is a noun
        if topic_check_pos_type(topic) != True:
            print(f'{topic} is not a noun. Skipping...')
            return []
        filename = filename_create(topic)
        topic_page = wikipedia.page(topic)
        topic_links = topic_page.links
        # save the keys to a file with the name of the page as the file name in the wikipedia_keys folder
        with open(f'./wikipedia_keys/{filename}.csv', 'w+') as f:
            for link in topic_links:
                f.write(f'{link}\n')
        #? While the page exists save the page text to a file with the name of the page as the file name in the wikipedia_pages folder
        while_page_exists(topic_page,filename)
    except Exception as e:
        topic_links = []

    return topic_links

def get_relevant_subtopics(parent_topic):
    # get the list of subtopics from the parent topic page.
    # get all links from the parent topic page
    global keys_dict
    # make sure that the topic page will show up in the search results
    parent_topic_links = get_links(parent_topic)
    #note: could use a for loop above until len(parent_topic_links) > 0

    # get the list of subtopics from the parent topic page.
    subtopics = []
    # if parent_topic_links is NoneType then check the keys_dict.csv file for the topic
    if parent_topic_links == None:
        # check the keys_dict.csv file for the topic
        subtopics = keys_dict[parent_topic]

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
        if len(subtopics_keywords[subtopic]) == 0:
            print('')
        else:
            print(f'Found {len(subtopics_keywords[subtopic])} keywords.')
        #//print(f'Found {len(subtopics_keywords[subtopic])}')

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

def clear_all_previously_saved_files():
    # delete all files in the wikipedia_pages folder
    for filename in os.listdir("wikipedia_pages"):
        os.remove(f"wikipedia_pages/{filename}")

def main():
    global N
    global master_dict

    print("\n\nWelcome to the Subtopic Finder!")
    print("This program will find subtopics for a given topic.")
    print("All subtopics will be saved (article text to the wikipedia_pages directory) and added to the master dictionary.")
    choice = input("\n  Would you like to clear previously generated articles? (y/n) ")
    if choice == "y":
        clear_all_previously_saved_files()

    print("Settings (Current):")
    print(f'N = {N} - The required minimum number of keywords in common between parent-child pages.')
    choice = input("Would you like to change settings? (y/n) ")
    if choice == "y":
        N = int(input("N = "))
        print(f'updated: N = {N}')

    print("Please wait while the program runs...")
    choice = input("Would you like to enter a topic (parent_page)? (y/n) ")
    if choice == "y":
        parent_page = input("Enter a topic: ")
    else:
        parent_page = "Nikola Tesla"


    print("Would you like to also generate a lorebook with the results of the subtopic finder? (y/n)")
    choice = input("(y/n): ")
    if choice == "y":
        generate_lorebook = True # flag to generate a lorebook
    else:
        generate_lorebook = False # flag to not generate a lorebook




    relevant_subtopics = get_relevant_subtopics(parent_page)
    # print(relevant_subtopics)
    if generate_lorebook:
        # create a new lorebook
        # to do this, save the subtopics we found to the characters.csv file and then run the lorebook generator
        # save the subtopics to the characters.csv file
        with open("./data/characters.csv", "w") as f:
            f.write(
                "Name,\n"
            )
            for subtopic in tqdm(relevant_subtopics):
                #& Remove commas from the subtopic names because they will mess up the csv file
                subtopic = subtopic.replace(",", "")
                #& Remove nonalpha numeric characters from the subtopic names because they will mess up the csv file
                subtopic = re.sub(r"[^a-zA-Z0-9]+", " ", subtopic) # remove all non-alphanumeric characters
                f.write(
                    f'{subtopic},\n'
                )
        # run the lorebook generator
        print("\nCharacters File has been updated!\n\nTo generate a new Lorebook, run the 03_lorebook_from_wiki_withpulls.py file.")

main()