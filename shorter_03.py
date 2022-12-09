import wikipedia
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

def preprocess(sent):
  sent = nltk.word_tokenize(sent)
  sent = nltk.pos_tag(sent)
  return sent

def examine_dates(entry1, entry2):
  article_one_dates = []
  article_two_dates = []

  for sent in sent_tokenize(entry1):
    for chunk in nltk.ne_chunk(preprocess(sent)):
      if hasattr(chunk, "label") and chunk.label() == "DATE":
        article_one_dates.append(" ".join(c[0] for c in chunk.leaves()))

  for sent in sent_tokenize(entry2):
    for chunk in nltk.ne_chunk(preprocess(sent)):
      if hasattr(chunk, "label") and chunk.label() == "DATE":
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

def find_unique_keys(keys_dict):
  # get all the keywords (across all entries) -> keyword_master_list
  keyword_master_list = [key for entry in keys_dict for key in keys_dict[entry]]

  # go through each row's keywords and keep them in one of two cases:
  # (1) if they occur only once in keyword_master_list or (2) if they occur more often than the minimum threshold
  unique_keys = []
  for entry in keys_dict:
    for key in keys_dict[entry]:
      if keyword_master_list.count(key) == 1 or keyword_master_list.count(key) >= minimum_key_occurrences:
        unique_keys.append(key)
  return unique_keys

# Global Variables Declaration
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
maxlinksperpage = 30
minimum_key_occurrences = 4
