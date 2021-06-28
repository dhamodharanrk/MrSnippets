__author__ = 'dhamodharan.k'
import xml.etree.ElementTree as ET
import ast
from xml.etree.ElementTree import Element, SubElement
from xml.sax.saxutils import escape

def pandas_to_xml(**kwargs):
    """
    A method used to convert pandas to solr xml
    :param kwargs: A keyword args mainly contains,
        dataFrame : pandas data frame object
        fileName : output file name
        list_variables : Values should considered as list
        xml_declaration : True/False by default True
    :return: he file will be stored in file directory
    """
    _IGNORE_ME = ['nan', '', 'NA', 'NaT', 'None', '[]']
    df = kwargs.get("dataFrame")
    fileName = kwargs.get("fileName")
    xml_declaration = kwargs.get("xml_declaration", True)
    file_path = kwargs.get("file_path", './')
    tree = ET.ElementTree()
    rootElement = Element('add')
    records = df.to_dict('rows')
    for dictRow in records:
        subDoc = SubElement(rootElement, 'doc')
        for key, value in dictRow.items():
            if str(value) not in _IGNORE_ME:
                if isinstance(value,list):
                    for textData in value:
                        if str(textData) not in _IGNORE_ME:
                            textData = str(textData)
                            current_group = SubElement(subDoc, "field", {'name': key})
                            current_group.text = escape(textData)
                elif isinstance(value,str):
                    value = str(value)
                    current_group = SubElement(subDoc, "field", {'name': key})
                    current_group.text = escape(value)
    tree._setroot(rootElement)
    tree.write(file_path + fileName, encoding='utf8', xml_declaration=xml_declaration, method='xml')

def create_xml_string_from_dict(data_dict:dict):
    xml_string = '<doc>\n'
    f_close = '</field>\n'
    for each_key in data_dict:
        if isinstance(data_dict[each_key], list) and len(data_dict[each_key]) > 0:  # this is for list members
            for element in data_dict[each_key]: # over elements of list members
                if element is not None:
                    for each_inner_key in element:  # over the keys of inner dict
                        if element[each_inner_key] is not None:
                            if element[each_inner_key]:
                                current_line = '<field name="' + each_inner_key + '">' + escape(
                                    element[each_inner_key]) + f_close
                                xml_string = xml_string + current_line
        if (not isinstance(data_dict[each_key], list)) and data_dict[each_key] is not None:
            current_line = '<field name="' + each_key + '">' + escape(str(data_dict[each_key])) + f_close
            xml_string = xml_string + current_line
    xml_string = xml_string + '</doc>\n'
    return xml_string