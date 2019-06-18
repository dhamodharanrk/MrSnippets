__author__ = 'dhamodharan.k'
import os
import re
import ftfy
from fuzzywuzzy import fuzz
import collections


# String Operations

def get_clean_text(string:str):
    '''Used to to remove the whitespace in given string such as tab,space,newlines and encoding issues'''
    string = ftfy.fix_text(string)
    string = re.sub('\s+', ' ', string)
    string = re.sub('\n|\t|^\s+\|\s+$', '', string)
    string = string.strip()
    return string

def get_numbers_from_string(string:str):
    '''Returns a number from given string'''
    num = ''.join([i for i in string if i.isnumeric()])
    return num

def get_alpha_from_string(string:str):
    '''Returns only alpha chars from given text'''
    except_list = list('/\."$*<>:|?')
    string = ''.join([i for i in string if i.isalpha() or i not in except_list])
    return string

def get_string_from_html(soup):
    '''removes hyperlinks and tags from string for text analysis process'''
    clean_string = re.sub("(<.*?>)", "", str(soup), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = re.sub("(<style.*?</style>)", "", str(clean_string), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = get_clean_text(clean_string)
    return  clean_string

def compare_string(string_one,string_two):
    '''compare two strings and returns a ratio of match in integer. Uses fuzz logic'''
    return fuzz.ratio(string_one,string_two)

def join_string(source_list:list, separator:str=' '):
    '''Joing list of items with given separator'''
    return separator.join(source_list)

def refine_name(name:str):
    reobj = re.compile(r'(?sm)((Dr|Ph\.D|Jr|LL\.M|Avv|\b[A-Z]{1}|\b[a-z]{1}|Prof)\.|\b(Dr|Jr|Ph\.D|LL\.M|PhD|LLM|Dipl.-Jur.|Jur|DAPI|\*|,\s*[A-Z]{2,4}|[A-Z]{1})(\s|$)|\(.*?\)|(".*?")|(/|;).*?$)')
    match = reobj.search(name)
    if match:
        refined_name = re.sub(r'(?sm)((Dr|Ph\.D|Jr|LL\.M|\b[A-Z]{1}|\b[a-z]{1}|Prof)\.|\b(Dr|Jr|Ph\.D|LL\.M|PhD|LLM|Dipl.-Jur.|Jur|DAPI|\*|,\s*[A-Z]{2,4}|[A-Z]{1})(\s|$)|\(.*?\)|(".*?")|(/|;).*?$)', '', name)
        refined_name = refined_name.replace('  ', ' ').strip()
    else: refined_name = get_clean_text(name)
    return refined_name

def split_name(name_string:str,reverse_it:bool=False,**kwargs):
    split_by = kwargs.get('split_by'," ")
    assert len(name_string.split(split_by)) > 1, "Given String is not splittable by given split_by key"
    nameData = {}
    name = ftfy.fix_text(refine_name(name_string))
    name_split = str(name).split(split_by)
    if reverse_it:
        name_split = list(reversed(name_split))
        name = " ".join(name_split)
    fname,lname = name_split[0],name_split[-1]
    nameData['FullName'] = name
    nameData['FirstName'] = fname
    nameData['LastName'] = lname
    return nameData

# List Operations
def get_clean_list(list_x:list):
    '''clean the list values using get_clean_text()'''
    return [get_clean_text(i) for i in list_x]

def compare_list(first:list, second:list):
    '''Compare first list with second and returns the difference'''
    second = set(second)
    return [item for item in first if item not in second]

def find_list_duplicates(list:list):
    '''Returns a duplicate values in list'''
    return [item for item, count in collections.Counter(list).items() if count > 1]

# Dict Operations
def get_clean_dict(dict:dict):
    '''passed through get_clean_text() for both keys and values'''
    for key, value in dict.items():
        dict[get_clean_text(str(key)) if type(key) == str else key] = get_clean_text(str(value)) if type(value) == str else value
    return dict

def modify_jsondata(abbreviations_dict:dict,target_dict:dict):
    '''{'name':'dharan'} to {'person_name':'dharan'}. here abbreviation dict has {'person_name':'name'}'''
    collected_data = {}
    for source_attribute, target_attribute in abbreviations_dict.items():
        if target_attribute:
            if target_attribute in target_dict:
                collected_data[source_attribute] = target_dict[target_attribute]
            else: collected_data[source_attribute] = abbreviations_dict[source_attribute]
        else:collected_data[source_attribute] = abbreviations_dict[source_attribute]
    return collected_data


