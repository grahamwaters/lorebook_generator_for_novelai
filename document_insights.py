import pandas as pd
import os
from tqdm import tqdm
# Goal:
# Open each text file in the Wikipedia pages directory and scan the text for paragraphs that contain multiple keywords from the keywords list
# Return a dictionary where the key is the list of keywords found and the value is the paragraph text

# create the blank dictionary
links = []
# create the list of keywords
keywords = ['Paris','1883','Tesla','hunting']

# for each file in the directory
for file in tqdm(os.listdir('wikipedia_pages')):
    # open the file
    with open('wikipedia_pages/' + file, 'r') as f:
        # read the file
        text = f.read()
        # split the text into paragraphs
        paragraphs = text.split('\n\n')
        # for each paragraph in the text
        for paragraph in paragraphs:
            # for each keyword in the keywords list
            for keyword in keywords:
                # if the keyword is in the paragraph and another keyword is also in the paragraph
                if keyword in paragraph:
                    for keyword2 in keywords:
                        if keyword != keyword2 and keyword2 in paragraph:
                            # if the keywords are not already in the dictionary

                            # add the keywords as a tuple and the paragraph text as the value
                            links.append([(keyword, keyword2), paragraph])
            #if all keywords are in the paragraph print it
            if all(keyword in paragraph for keyword in keywords):
                print(paragraph)


# save the dictionary as a csv file
pd.DataFrame(links).to_csv('paragraphs.csv')
