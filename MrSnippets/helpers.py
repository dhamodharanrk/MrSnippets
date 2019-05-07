__author__ = 'dhamodharan.k'
import os
import re

def get_clean_text(string:str):
    clean_string = string.replace('\n', '').replace('\t', '').replace('\r', '').strip()
    clean_string = ' '.join(clean_string.split())
    return clean_string

def get_numbers(string):
    num = ''.join([i for i in string if i.isnumeric()])
    return num

def get_alpha(string):
    except_list = list('/\."$*<>:|?')
    string = ''.join([i for i in string if i.isalpha() or i not in except_list])
    return string

def get_clean_list(i_list):
    j_list = []
    for i in i_list:
        clean_string = i.replace('\n', '').replace('\t', '').replace('\r', '').strip()
        j_list.append(clean_string)
    return j_list

def get_json_value(json_chunk,key):
    if str(key) in json_chunk:
        value = json_chunk[key]
        if "'" in str(value) and type(value) is str:
            value = value.replace("'", '"')
    else:
        value = None
    return value

def clean_dict(dict):
    for key, value in dict.items():
        dict[key] = get_clean_text(str(value)) if type(value) == str else value
    return dict

def get_string_from_html(soup):
    clean_string = re.sub("(<.*?>)", "", str(soup), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = re.sub("(<style.*?</style>)", "", str(clean_string), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = get_clean_text(clean_string)
    return clean_string

def convert_base64_Image(encoded_data,path,file_name,):
    try:
        import base64
        if not os.path.exists(path):
            os.makedirs(path)
        imgdata = base64.b64decode(encoded_data)
        with open(path + file_name + '.jpg', 'wb') as f:
            f.write(imgdata)
    except Exception as error:
        return error