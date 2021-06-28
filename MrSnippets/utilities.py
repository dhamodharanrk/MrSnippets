__author__ = 'dhamodharan.k'
import re
import ftfy
import xml.etree.ElementTree as ET
from fuzzywuzzy import fuzz
import inspect
import collections
from user_agent import generate_user_agent
from dateutil import parser
from os import path
import os
from bs4 import BeautifulSoup
import csv
import uuid
from datetime import datetime
import shutil
import hashlib
import glob


def get_clean_text(string:str):
    """
    :param string: takes raw string
    :return: returns clean string and tab,space,newlines,encoding issues fixed

    """
    string = ftfy.fix_text(string)
    # string = re.sub('\s+', ' ', string)
    # string = re.sub('\n|\t|^\s+\|\s+$', '', string)
    # string = string.strip()
    return string

def get_clean_html(html_chunk):
    '''
    Method to clean the given HTML Chunk and returns the cleaned version of HTML
    :param soup: raw HTML chunk
    :return: Cleaned HTML Chunk

    '''
    soup = str(html_chunk)
    clean_data = re.sub("(<img.*?>)", "", soup, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_data = re.sub("(<input.*?>)", "", clean_data, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_data = re.sub('(href=".*?")', "", clean_data, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_data = re.sub('(<script .*?</script>)', "", clean_data, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_data = re.sub('(<!--.*?-->)', "", clean_data, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = str(clean_data).replace('\n', '').replace('\t', '').replace('\r', '').replace('\xa0',' ').strip()
    clean_string = clean_string.replace('Click here', '').replace('Read More', '')
    clean_string = clean_string.replace('<button', '<div').replace('</button>', '')
    clean_string = ' '.join(clean_string.split())
    clean_string = ftfy.fix_text(clean_string)
    clean_string = ftfy.fix_text_encoding(clean_string)
    soup = BeautifulSoup(clean_string, 'lxml')
    for tags in soup.find_all():
        if not tags.text:
            tags.decompose()
    clean_string = str(soup)
    return clean_string

def get_string_from_html(html_chunk):
    """
    :param html_chunk: Takes HTML chunks
    :return: removes hyperlinks and tags from string for text analysis process
    """
    clean_string = re.sub("(<.*?>)", "", str(html_chunk), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = re.sub("(<style.*?</style>)", "", str(clean_string), 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    clean_string = get_clean_text(clean_string)
    return  clean_string

def get_numbers_from_string(string:str):
    """
    :param string: takes a string as input
    :return: returns numbers from given string
    """
    num = ''.join([i for i in string if i.isnumeric()])
    return num

def get_alpha_from_string(string:str):
    """
    :param string: takes are string as input
    :return: returns only alpha chars from given text
    """
    except_list = list('/\."$*<>:|?')
    string = ''.join([i for i in string if i.isalpha() or i not in except_list])
    return string

def compare_two_strings(string_one,string_two):
    """
    :param string_one: any text string
    :param string_two: any text string
    :return: returns match ratio in integer using fuzzy logic
    """
    return fuzz.ratio(string_one,string_two)

############################## LIST Operations ##############################

def join_elements(source_list:list, separator:str=' '):
    """
    :param source_list: Takes list as input
    :param separator: any special chars or any printable chars
    :return: join given list elements with given separator and returns a string
    """
    return separator.join(source_list)

def get_clean_list(list_x:list):
    '''clean the list values using get_clean_text()'''
    return [get_clean_text(i) for i in list_x]

def compare_two_list(first:list, second:list):
    '''Compare first list with second and returns the difference'''
    second = set(second)
    return [item for item in first if item not in second]


def find_duplicates_from_list(list:list):
    '''Returns a duplicate values in list'''
    return [item for item, count in collections.Counter(list).items() if count > 1]

def get_unique_values(sequence:list):
    '''
    Get unique list values without loosing the order
    :param sequence: python list [1,4,7,9,0,1,4,6,7]
    :return: returns python unique ordered list [1,4,7,9,0,6,7]
    '''
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


############################## Dict Operations ##############################


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
            if target_attribute in target_dict:collected_data[source_attribute] = target_dict.get(target_attribute, '')
            else:collected_data[source_attribute] = ''
        else: collected_data[source_attribute] = ''
    collected_data = {key: value for key, value in collected_data.items() if str(key) != str(value)}
    return collected_data


def combine_dict(dict1, dict2):
    '''
    Merge dictionaries and keep values of common keys in list

    :param dict1: {'fruit':'apple','name':'dharan'}

    :param dict2: {'fruit':'Orange'}

    :return:  {'fruit':['apple','Orange'],'name':'dharan'}

    '''
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = [value, dict1[key]]
    return dict3

############################## Support Operations ##############################

def get_current_user_name():
    try:
        try:
            import pwd
            user_name = pwd.getpwuid(os.geteuid()).pw_name
        except ImportError:
            import getpass
            user_name = getpass.getuser()
    except: user_name = None
    return user_name

def get_current_platform():
    '''
    A method to find the current working operating system/platform

    :return: any one of linux/os x/windows
    '''
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        return "os x"
    elif platform == "win32":
        return "windows"

def get_class_variables(class_obj):
    '''Simple method to get the list of variable from the given class object'''
    variables = list(class_obj.__dict__.keys())
    return variables

def get_current_script_name():
    """
    Simple method used to get the calling function name.
    :return: returns callers script name without file extension
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    filename = str(filename).split("/")[-1].split('.')[0]
    return filename

def get_user_agent(**kwargs):
    domain_specific = {}
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    try:
        domain_name = kwargs.get('domain_name','NA')
        user_agent = domain_specific.get(domain_name) if domain_name in domain_specific.keys() else generate_user_agent(device_type='desktop',os=['win','linux','mac'])
    except: pass
    return user_agent

def generate_fileName(project, ext):
    time_ = datetime.now().isoformat(sep="_").split(".")[0].replace(':', '.')
    if project:
        fileName = "export_{}_{}.{}".format(project, time_, ext)
    else:
        fileName = "export_{}.{}".format(time_, ext)
    return fileName

def generate_uuid_by_digits(digits):
    """
    Returns the unique identifier for given number of digits

    :param digits: int value holds number of digits needs to be returned

    :return:
    """
    return uuid.uuid4().hex[:int(digits)].upper()

def genearate_hash_key(string):
    '''
    Generate the Hash string out of given string

    :param string: Any string value

    :return: md5 hexdigest string
    '''
    h = hashlib.md5(str(string).encode())
    return h.hexdigest()


############################## File Operations ##############################

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

def get_filename(file_name):
    '''Used to get file name from the path'''
    temp = str(file_name).lower().split("\\")[-1].split('.')
    if len(temp)>=2:
        return "{}.{}".format(temp[0],temp[1])
    else: return None

def move_to(source,destination,filename):
    '''Used to move the file from source to destination'''
    shutil.move(source, destination + "\\" + filename)

def copy_to(source,destination,filename):
    '''Used to copy the file from source to destination'''
    shutil.copy(source, destination + "\\" + filename)

def list_files(diretory,ext:str=''):
    '''List all the files in the directory'''
    if ext: return glob.glob(diretory + "\\*." + str(ext))
    else: return glob.glob(diretory + "\\*.*")

def read_text_file(file_name):
    try:
        with open(file_name,'r', encoding='utf8') as fileReadObj:
            rows = fileReadObj.read()
            return rows
    except:
        with open(file_name,'r', encoding='ISO-8859-1') as fileReadObj:
            rows = fileReadObj.read()
            return rows

def read_xml_file(path,file):
    parser = ET.XMLParser(encoding='utf-8')
    mytree = ET.parse(path + file, parser=parser)
    myroot = mytree.getroot()
    return mytree, myroot

def read_xml_file_as_bs4(path,file_name):
    with open(os.path.join(path, file_name), 'r', encoding='utf-8') as file_handler:
        soup = BeautifulSoup(file_handler.read(), 'xml')
    return soup

def write_text_file(filepath, filename, content):
    filepath = os.getcwd() if filepath == '' else filepath
    with open(filepath + "/" + filename, 'a', encoding='utf8') as fileWriteObj:
        fileWriteObj.write(str(content) + "\n")

def write_csv_file(filepath,filename,content:dict,headers:list):
    filepath = os.getcwd() if filepath == '' else filepath
    with open(filepath + "/" + filename, 'a', encoding='utf8') as fileWriteObj:
        writer_ptr = csv.DictWriter(fileWriteObj, delimiter='\t',fieldnames=headers)
        writer_ptr.writerow(content)

def check_file_exists(file_dir):
    '''
    Simple method to check the existence of the given file.

    :param file_dir: file path

    :return: Bool value
    '''
    return path.exists(file_dir)

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


################## Date Operations #######################


def get_current_date(format="ISO"):
    if format== "ISO":
        return datetime.now().isoformat()
    else:
        return str(datetime.now().strftime("%d_%m_%Y"))

def get_yearFromDate(self, date_string):
    '''
    The method used to get year from the given date string
    :param date_string: any date string
    :return: int year from given date string
    '''
    year = 0
    try:
        t = parser.parse(date_string)
        year = t.year
    except:
        pass
    return int(year)

def convert_date_to(input_string, format):
    '''
    A method used to convert the date string in given format
    :param input_string: Date String
    :param format: format name which date string need to be converted.Currently supports,
        iso : converts date into iso date format
    :return: converted date in required format
    '''
    converted = input_string
    t = parser.parse(input_string)
    if format == 'iso': converted = str(t.isoformat())
    return converted

########################### Email functions ####################################

def send_email_with_attachment(projectName, userMessage, attachment, recipients,default_email_recipients=''):
    """
    A email method used to send the attachments with given information
    :param projectName: Project Name should mentioned in the subject
    :param userMessage: Email Body
    :param attachment: Attachment file path
    :param recipients: email recipients separated by comma
    :return: None
    """
    if attachment:
        today_date = str(datetime.now().strftime("%d/%m/%Y"))
        Subject = "Automated Alert {}:{}".format(projectName, today_date)
        message = "'Hi All,\n\n " + userMessage + "\n\n Thanks, \n MrSnippets'"
        if recipients:
            os.system("echo " + message + " | mail -s '" + str(Subject) + "' -c " + str(default_email_recipients) + " -a " + attachment + " " + recipients)
        else:
            os.system("echo " + message + " | mail -s '" + str(Subject) + "'" + " -a " + attachment + " " + default_email_recipients)

def email_notification(notificationType, project, message, recipients,default_email_recipients=''):
    """
    Method used to send the email using linux's mail method with user given values
    :param notificationType: Type of the notification. which will be mentioned in the subject
    Planed Options,
        1. INFO
        2. ERROR
        3. ALERT
        4. WARNING
    Example : <TYPE> Notification: <PROJECT> --> INFO Notification : AIMS
    :param project: Project Name
    :param message: Mail Body
    :return: None
    """
    subject = "{} Notification : {}".format(notificationType, project)
    message = "'Hi All,\n\n " + message + ".\n\n Thanks, \n MrSnippets'"
    os.system("echo " + message + " | mail -s '" + str(subject) + "' -c " + str(default_email_recipients) + " " + recipients)