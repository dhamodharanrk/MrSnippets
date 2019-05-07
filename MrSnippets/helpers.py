__author__ = 'dhamodharan.k'
import os
import re

def get_clean_text(string:str):
    clean_string = string.replace('\n', '').replace('\t', '').replace('\r', '').strip()
    clean_string = ' '.join(clean_string.split())
    return clean_string

def get_numbers_from_string(string:str):
    num = ''.join([i for i in string if i.isnumeric()])
    return num

def get_alpha_from_string(string:str):
    except_list = list('/\."$*<>:|?')
    string = ''.join([i for i in string if i.isalpha() or i not in except_list])
    return string

def get_clean_list(list_x:list):
    list_y = []
    for i in list_x:
        clean_string = i.replace('\n', '').replace('\t', '').replace('\r', '').strip()
        list_y.append(clean_string)
    return list_y

def get_clean_json_string(json_chunk,key):
    if str(key) in json_chunk:
        value = json_chunk[key]
        if "'" in str(value) and type(value) is str:
            value = value.replace("'", '"')
    else:
        value = None
    return get_clean_text(value)

def clean_dict(dict):
    for key, value in dict.items():
        dict[key] = get_clean_text(str(value)) if type(value) == str else value
    return dict

def get_string_from_html(soup):
    clean_string = re.sub("(<.*?>)", "", str(soup), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = re.sub("(<style.*?</style>)", "", str(clean_string), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = get_clean_text(clean_string)
    return clean_string

def convert_base64_Image(encoded_data,path_to_store,file_name):
    try:
        import base64
        if not os.path.exists(path_to_store):
            os.makedirs(path_to_store)
        imgdata = base64.b64decode(encoded_data)
        with open(path_to_store + file_name + '.jpg', 'wb') as f:
            f.write(imgdata)
    except Exception as error:
        return error