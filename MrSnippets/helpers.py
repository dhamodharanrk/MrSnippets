__author__ = 'dhamodharan.k'
import os
import re
import ftfy
import collections


# String Operations

def get_clean_text(string:str):
    string = ftfy.fix_text(string)
    string = re.sub('\s+', ' ', string)
    string = re.sub('\n|\t|^\s+\|\s+$', '', string)
    string = string.strip()
    return string

def get_numbers_from_string(string:str):
    num = ''.join([i for i in string if i.isnumeric()])
    return num

def get_alpha_from_string(string:str):
    except_list = list('/\."$*<>:|?')
    string = ''.join([i for i in string if i.isalpha() or i not in except_list])
    return string

def get_string_from_html(soup):
    clean_string = re.sub("(<.*?>)", "", str(soup), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = re.sub("(<style.*?</style>)", "", str(clean_string), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = get_clean_text(clean_string)
    return  clean_string

def join_string(source_list:list, separator:str=' '):
    return separator.join(source_list)

# List Operations
def get_clean_list(list_x:list):
    return [get_clean_text(i) for i in list_x]

def compare_list(first:list, second:list):
    second = set(second)
    return [item for item in first if item not in second]

def find_list_duplicates(list:list):
    return [item for item, count in collections.Counter(list).items() if count > 1]

# Dict Operations
def get_clean_dict(dict:dict):
    for key, value in dict.items():
        dict[get_clean_text(str(key)) if type(key) == str else key] = get_clean_text(str(value)) if type(value) == str else value
    return dict


