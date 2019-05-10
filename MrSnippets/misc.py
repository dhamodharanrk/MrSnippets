__author__ = 'dhamodharan.k'
import os
import pickle
import csv

from urllib.parse import urlparse
current_path = os.getcwd()

def read_text_file(file_name):
    try:
        with open(file_name,'r', encoding='utf8') as fileReadObj:
            rows = fileReadObj.read()
            return rows
    except:
        with open(file_name,'r', encoding='ISO-8859-1') as fileReadObj:
            rows = fileReadObj.read()
            return rows

def write_text_file(filepath, filename, content):
    filepath = os.getcwd() if filepath == '' else filepath
    with open(filepath + "/" + filename, 'a', encoding='utf8') as fileWriteObj:
        fileWriteObj.write(str(content) + "\n")

def write_csv_file(filepath,filename,content:dict,headers:list):
    filepath = os.getcwd() if filepath == '' else filepath
    with open(filepath + "/" + filename, 'a', encoding='utf8') as fileWriteObj:
        writer_ptr = csv.DictWriter(fileWriteObj, delimiter='\t',fieldnames=headers)
        writer_ptr.writerow(content)

def get_base64Image(encoded_data,path_to_store,file_name):
    try:
        import base64
        if not os.path.exists(path_to_store):
            os.makedirs(path_to_store)
        imgdata = base64.b64decode(encoded_data)
        with open(path_to_store + file_name + '.jpg', 'wb') as f:
            f.write(imgdata)
    except Exception as error:
        return error

def get_city_list():
    try:
        with open(current_path + "\\data\\cities.pickle",'rb') as f:
            cities_data = pickle.load(f)
            return list(cities_data.City)
    except: return []

def get_state_list():
    try:
        with open(current_path + "\\data\\cities.pickle",'rb') as f:
            cities_data = pickle.load(f)
            return list(set(cities_data.State))
    except: return []

def get_city_info_obj():
    try:
        with open(current_path + "\\data\\cities.pickle", 'rb') as f:
            cities_data = pickle.load(f)
            return cities_data
    except: return None

def get_sizeof(num, suffix='o'):
    """Readable file size
    :param num: Bytes value
    :type num: int
    :param suffix: Unit suffix (optionnal) default = o
    :type suffix: str
    :rtype: str
    """
    for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def get_current_user():
    try:
        try:
            import pwd
            user_name = pwd.getpwuid(os.geteuid()).pw_name
        except ImportError:
            import getpass
            user_name = getpass.getuser()
    except: user_name = None
    return user_name

def get_parsed_url(url_to_parse):
    return urlparse(url_to_parse)