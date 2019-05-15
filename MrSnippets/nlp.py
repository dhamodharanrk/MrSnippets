__author__ = 'dhamodharan.k'
import bleach
import re
from collections import Counter
from nltk.corpus import stopwords
from MrSnippets.helpers import *

# Use Python console to download stopwords
# import nltk
# nltk.download('stopwords')

def clean_my_html(html_source):
    CleanText = bleach.clean(html_source, tags=[], attributes={}, styles=[], strip=True)
    CleanText = get_clean_text(CleanText)
    symbol_list = ['"', '!', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=','>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    for symbol in symbol_list: CleanText = CleanText.replace(symbol, ' ')
    CleanText = ''.join(i for i in CleanText if ord(i) < 128)
    CleanText = CleanText.lower()
    word_source = [word.strip() for word in CleanText.split() if len(word) != 1 and not word.isdigit() and len(word) != 2]
    return [word_source, CleanText]

def get_top_keywords(self, html_source):
    word_source = self.html_cleaning(html_source)
    stopwords_set = stopwords.words("english")
    words_without_stopwords = [word for word in word_source[0] if stopwords_set.count(word) < 1]
    counts = Counter(words_without_stopwords)
    counts = [(k, counts[k]) for k in sorted(counts, key=counts.get, reverse=True)]
    TopTenWords = {str(list(items)[0]): str(list(items)[1]) for items in counts[0:10]}
    return TopTenWords

def get_word_frequency(html_source, search_words):
    # search_words = ['with','very']
    # search_words = {'verbs': 'and,or,the,why,what', 'names': 'an,hello,analysis'}
    word_frequency = {}
    word_source = clean_my_html(html_source)
    if str(type(search_words)).__contains__('list'):
        for keyword in search_words:
            if len(keyword.split()) == 1:
                word_frequency[str(keyword)] = str(word_source[0].count(keyword.lower().strip()))
            else:
                word_frequency[str(keyword)] = str(word_source[1].count(keyword.lower().strip()))
    elif str(type(search_words)).__contains__('dict'):
        for labels in search_words.keys():
            counter = 0
            for keyword in str(search_words[labels]).split(','):
                if len(keyword.split()) == 1:
                    counter += word_source[0].count(keyword.lower().strip())
                else:
                    counter += word_source[0].count(keyword.lower().strip())
            word_frequency[labels] = str(counter)
    return word_frequency