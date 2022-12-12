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
            # if is_person:
            #     print(f'person found: {page2.title}')
            # if is_event:
            #     print(f'event found: {page2.title}')
            # if is_location:
            #     print(f'location found: {page2.title}')
            #ignore if not a person, event, or location
            if is_location or is_event or is_person:

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
    # save the paragraphs to a temporary txt file
    try:
        with open('../data/ai_identified_paragraphs.txt', 'w') as f:
            for key, value in paragraphs.items():
                f.write("%s:%s \n" % (key, value)) # write the key and value to the file
    except Exception as e:
        print(e)
    return paragraphs

# Extract the paragraphs from the parent page of the first feature, that mention the second feature.
# The first feature is the parent page of the second feature.
paragraphs = extract_paragraphs("England", "Tesla")
try:
    paragraphs2 = extract_paragraphs("France", "Tesla")
    paragraphs3 = extract_paragraphs("Germany", "Tesla")
    paragraphs4 = extract_paragraphs("Italy", "Tesla")

    # concatenate the paragraphs dictionaries into one dictionary, if duplicate keys exist then replace one of them with the name + 2
    paragraphs.update(paragraphs2)
    paragraphs.update(paragraphs3)
    paragraphs.update(paragraphs4)
except Exception as e:
    print(e)

# save the extracted paragraphs to a csv file
df = pd.DataFrame.from_dict(paragraphs, orient='index', columns=["link", "paragraph"])
df.to_csv("../data/ai_identified_paragraphs.csv", index=False)

# Print the extracted paragraphs
for link, paragraph in paragraphs.items():
    print(f"Paragraph from '{link}' page:")
    print(paragraph)
