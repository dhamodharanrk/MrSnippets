__author__ = 'dhamodharan.k'
import nltk
from geotext import GeoText
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import nltk.classify.util
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer
from MrSnippets import utilities as util
from nltk.tokenize import SExprTokenizer
import string
import spacy

nlp = spacy.load("en_core_web_sm")

try:
    stop_words = set(stopwords.words('english'))
except:
    raise FileNotFoundError("Stopwords not Found! use \n import nltk\nnltk.download('stopwords')\n in the python console")

# Use Python console to download stopwords
# import nltk
# nltk.download('stopwords')

# Support functions

def _remove_stopwords(word_tokens:list):
    """
    :param word_tokens:
    :return:
    """
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence

def _normalize_text(text:str):
    """
    :param text:
    :return:
    """
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    updated_text = text.lower()
    updated_text = util.get_clean_text(updated_text)
    updated_text = updated_text.translate(remove_punctuation_map)
    tokens = get_tokenized(updated_text,True,'word')
    return get_stemming(tokens)

def _create_frequency_table(text_string) -> dict:
    """
    we create a dictionary for the word frequency table.
    For this, we should only use the words that are not part of the stopWords array.
    Removing stop words and making frequency table
    Stemmer - an algorithm to bring words to its root word.
    :rtype: dict
    """
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()
    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    return freqTable

def _score_sentences(sentences, freqTable) -> dict:
    """
    score a sentence by its words
    Basic algorithm: adding the frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """
    sentenceValue = dict()
    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        word_count_in_sentence_except_stop_words = 0
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_except_stop_words += 1
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        if sentence[:10] in sentenceValue:
            sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] / word_count_in_sentence_except_stop_words
    return sentenceValue

def _find_average_score(sentenceValue) -> float:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]
    average = (sumValues / len(sentenceValue))
    return average

def _generate_summary(sentences:str, sentenceValue, threshold):
    sentence_count = 0
    summary = ''
    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1
    return summary

# Basic NLP Operations
def get_tokenized(sentence: str, ignore_stopwords: bool = False,use:str='SExpr'):
    """
    :param sentence:
    :param ignore_stopwords:
    :param use:
    :return:
    """
    word_tokens = []
    if use=="word": word_tokens = word_tokenize(sentence)
    if use=="SExpr":
        tk = SExprTokenizer()
        word_tokens = tk.tokenize(sentence)
    if ignore_stopwords:
        filtered_sentence = _remove_stopwords(word_tokens)
        return filtered_sentence
    else:
        return word_tokens

def sentence_tokenization(raw_text:str):
    """
    :param raw_text:
    :return:
    """
    return sent_tokenize(raw_text)

def get_stemming(word_tokens:list):
    """
    Stemming is the process of reducing the words(generally modified or derived) to their word stem or root form.
    The objective of stemming is to reduce related words to the same stem even if the stem is not a dictionary word.

    :param word_tokens: unprocced word tokens
    :return: processed list
    """
    ps = PorterStemmer()
    return [ps.stem(w) for w in word_tokens]

def get_lemmatize_data(word_tokens: list):
    """
    Lemmatisation is the process of reducing a group of words into their lemma or dictionary form
    :param word_tokens:
    :return:
    """
    lem = WordNetLemmatizer()
    return [lem.lemmatize(w) for w in word_tokens]

def get_standardize_words(tokens: list, lookup_dict: dict):
    """
    :param tokens:
    :param lookup_dict:
    :return:
    """
    new_words = []
    for word in tokens:
        if word.lower() in lookup_dict:
            word = lookup_dict[word.lower()]
        new_words.append(word)
    return new_words

def generate_ngrams(tokens: list, n):
    """
    :param tokens:
    :param n:
    :return:
    """
    output = []
    for i in range(len(tokens) - n + 1):
        output.append(tokens[i:i + n])
    return output

def generate_pos_tags(sentence, ignore_stopwords: bool = False):
    """
    :param sentence:
    :param ignore_stopwords:
    :return:
    """
    tokens = get_tokenized(sentence, ignore_stopwords)
    pos_tagged = nltk.pos_tag(tokens)
    return pos_tagged

def generate_named_entity(sentence):
    """
    :param sentence:
    :return:
    """
    doc = nlp(sentence)
    data = []
    for ent in doc.ents:
        dict_data = {}
        dict_data['TEXT'] = ent.text
        dict_data['START'] = ent.start_char
        dict_data['END'] = ent.end_char
        dict_data['LABEL'] = ent.label_
        data.append(dict_data)
    return data

def sentiment_analysis(sentence,algorithm:str="VADER"):
    """
    :param sentence:
    :param algorithm:
    :return:
    """
    sid = SentimentIntensityAnalyzer()
    sentiment_result = sid.polarity_scores(sentence)
    return sentiment_result

def get_cosine_similarity(text1:str, text2:str):
    """
    :param text1:
    :param text2:
    :return:
    """
    vectorizer = TfidfVectorizer(tokenizer=_normalize_text, stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def extract_geo_data(text:str,required='country'):
    """
    :param text:
    :param required:
    :return:
    """
    data = []
    if required == "countries":
        data = GeoText(text).countries
    if required == "cities":
        data = GeoText(text).cities
    if required == "nationalities":
        data = GeoText(text).nationalities
    return data

def generate_text_summary(text:str):
    freq_table = _create_frequency_table(text)
    sentences = sent_tokenize(text)
    sentence_scores = _score_sentences(sentences, freq_table)
    threshold = _find_average_score(sentence_scores)
    summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)
    return summary