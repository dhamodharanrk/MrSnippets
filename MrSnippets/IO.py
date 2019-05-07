__author__ = 'dhamodharan.k'
import os

def read_file(file_name):
    try:
        with open(file_name,'r', encoding='utf8') as fileReadObj:
            rows = fileReadObj.read()
            return rows
    except:
        with open(file_name,'r', encoding='ISO-8859-1') as fileReadObj:
            rows = fileReadObj.read()
            return rows

def write_file(filepath, filename, content):
    filepath = os.getcwd() if filepath == '' else filepath
    with open(filepath + "/" + filename, 'a', encoding='utf8') as fileWriteObj:
        fileWriteObj.write(content)