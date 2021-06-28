# MrSnippets

A complete collection of commonly used code Snippets in Python

## Getting Started

To get started, install the package using the below command on your machine.

`pip install MrSnippets`

Sample Usage,

    from MrSnippets.utilities import *
    print(get_numbers_from_string('1a2b3e'))
	>123

## Utilities Module

Its a collection of commonly used functions to minimize the coding effort and time.

#### List of supported functions,
##### Text Operations
- get_clean_text(string:str)
- get_clean_html(html_chunk)
- get_numbers_from_string(string:str)
- get_alpha_from_string(string:str)
- get_string_from_html(soup)
- compare_two_strings(string_one,string_two)

##### List Operations
- join_elements(source_list:list, separator:str='')
- get_clean_list(list_x:list)
- compare_two_list(first:list, second:list)
- find_duplicates_from_list(list:list)
- get_unique_values(	sequence:list)

##### Dict Operations
- get_clean_dict(dict:dict)
- modify_jsondata(abbreviations_dict:dict,target_dict:dict)
- combine_dict(dict1, dict2)

##### Support Functions
- get_current_user_name()
- get_current_platform()
- get_current_script_name()
- get_user_agent(**kwargs)
- generate_uuid_by_digits(digits)
- genearate_hash_key(string)
- generate_fileName(project, ext)
- get_class_variables(class_obj)

##### Date Operations

- get_current_date(format="ISO")
- get_yearFromDate(self, date_string)
- convert_date_to(input_string, format)

##### File Operations
- get_base64Image(encoded_data,path_to_store,file_name)
- get_filename(file_name)
- move_to(source,destination,filename)
- copy_to(source,destination,filename)
- list_files(diretory,ext:str='')
- read_text_file(file_name)
- read_xml_file(path,file)
- read_xml_file_as_bs4(path,file_name)
- write_text_file(filepath, filename, content)
- write_csv_file(filepath,filename,content:dict,headers:list)
- get_sizeof(num, suffix='o')
- check_file_exists(file_dir)

##### Email Functions
Some common functions to send an email from linux servers.

- send_email_with_attachment(projectName, userMessage, attachment, recipients,default_email_recipients='')
- email_notification(notificationType, project, message, recipients,default_email_recipients='')

## Data Mining Module

Its a simple implementation of CSS selector using Beautifulsoup. The selectors are straight forward and simple to use.

There is a list of pre-defined selector functions. For example, selecting a single element from a chunk as follows.

    from MrSnippets.soup_wrapper import  *
    people_name = get_element(html_chunk,'div','class','people_name')
    people_name = get_element_by_tag(html_chunk,'<div class="people_name">')


#### List of supported functions,
##### Bs4 Object based functions
- get_element(soup, tag="div", attributeName='class', attributeValue='profile')
- get_elements(soup, tag="div", attributeName='class', attributeValue='profiles')
- get_element_by_tag(soup,selector_string:str)
- get_elements_by_tag(soup,selector_string:str)
- get_sibling_text(soup, child:str, sibling:str, contains_string:str, sibling_type="prev|next")

##### Semi-Automated Functions

- extract_hyper_link(soup_chunk,patterns:list,**kwargs)
- extract_social_links(self, html_source)
- extract_vcard_link(soup_chunk,**kwargs)
- extract_image_link(soup_chunk,**kwargs)
- extract_vcard_data(vcard_text:str)
- extract_meta_data(self, html_source)
- extract_email_addresses(string)
- extract_phone_numbers(html_chunk)
- extract_domain_name_from_url(url)
- extract_date_from_string(date_string: str)
- extract_countries_from_text(input_text)
- extract_url_prefix(url_string: str)

##### Support Functions
- get_parsed_url(url_string)
- fix_url_format(self, url, prefix)
- validate_url(url)

##### Data Manipulations
- get_standard_name(name:str)
- split_name(name_string:str,reverse_it:bool=False,**kwargs)


## Web Clinet Moudule

Its an collection of commonly used function for interacting on Internet

#### List of supported functions,

- get_selenium_response(url, timeout)
- get_response(url, response_type, attempt=0, **kwargs)
- download_file(url,dir,file_name,extension)

**get_reponse** function utilized in many ways, these are the currently supported arguments,

    data = kwargs.get('data',{})
	params = kwargs.get('params',{})
	gateway = kwargs.get('gateway', 'requests')
    timeout = kwargs.get('time_out', 60)
    verify = kwargs.get('verify', True)
    method = kwargs.get('method', None)
    domain = kwargs.get('domain', '')
    headers = kwargs.get('headers',{})
    allow_redirects = kwargs.get('allow_redirects', True)
    proxy =  kwargs.get('proxy', True)
    stream =  kwargs.get('stream', False)
    dom_parser = kwargs.get('dom_parser','html5lib')

###### Sample Usage:

response = get_response(url,'json',method='post', data = payload, headers=headers, timeout=100, verify=False)


## NLP Module

Collection of functions to minimize the code and time for NLP related operations.

#### List of supported functions,

##### Main Functions
- sentence_tokenization(raw_text:str)
- get_tokenized(sentence: str, ignore_stopwords: bool = False,use:str='SExpr')
- get_stemming(word_tokens:list)
- get_lemmatize_data(word_tokens: list)
- get_standardize_words(tokens: list, lookup_dict: dict)
- generate_ngrams(tokens: list, n)
- generate_pos_tags(sentence, ignore_stopwords: bool = False)
- generate_named_entity(sentence)
- get_cosine_similarity(text1:str, text2:str)
- sentiment_analysis(sentence,algorithm:str="VADER")
- generate_text_summary(text:str)
- extract_geo_data(text:str,required='country')

##### Support Functions
- _remove_stopwords(word_tokens:list)
- _normalize_text(text:str)
- _create_frequency_table(text_string)
- _score_sentences(sentences, freqTable)
- _find_average_score(sentenceValue)
- _generate_summary(sentences:str, sentenceValue, threshold)

## Image Processing Module

Collection of  functions to minimize the code and time for image processing tasks

#### List of supported functions,
- adjust_brightness(input_image, output_image, factor)
- adjust_contrast(input_image, output_image, factor)
- adjust_sharpness(input_image, output_image, factor)
- resize_image(input_image_path,output_image_path,size)
- scale_image(input_image_path,output_image_path,width=None,height=None)
- black_and_white(input_image_path,output_image_path)
- rotateImage(image_path, degrees_to_rotate, saved_location)
- flipImage(image_path, saved_location,direction)
- cropImage(image_path, coords, saved_location)

## Data Support Module

Collection of functions to minimize the code and time for day to day tasks

#### List of supported functions,
- get_city_list()
- get_state_list()
- get_city_info_obj()

## Data Convertion Module

A collection of methods used to convert data files from one format to another.
For example, DataFrame to XML

#### List of supported functions,
- pandas_to_xml(**kwargs)
parameters for the functions includes,
```python
dataFrame : pandas data frame object
fileName : output file name
list_variables : Values should considered as list
xml_declaration : True/False by default True
```
- create_xml_string_from_dict(data_dict:dict)

## Mongo Wrapper
Its a collection of commonly used functions to minimize the code and time for mongo related operations.

To Setup, the Client IP do follow the below steps,

1. **from MrSnippets.mongo_wrapper import MONGO_CLIENT_IP**
2. Now, **CTRL + Right Click** on **MONGO_CLIENT_IP**
3. Update this *'xx.xx.xx.xxx'* to Your IP (195.16.20.335:27017)

now the line looks something like this,

`MONGO_CLIENT_IP = '195.16.20.335:27017'`

#### List of supported functions,

- get_mongo_client(database_name, collection_name)
- list_db()
- list_collections(db:str)
- get_summarize(db:str,collection:str)
- get_sample(db:str,collection:str,query_by:str,value:str,limit:int=1)
- update_record(connection:dict,query_by:str,query_by_value,data:dict)
- create_index(connection:dict,index_attributes:list,ascending:bool=True)
- update_attribute(connection:dict,query_by:str,query_by_value,data:dict,attributes:list)

## MySQL Wrapper

Its a collection of commonly used functions to minimize the code and time for MySQL related operations.

#### List of supported functions,

- get_mysql_client(host_ip, username, pwd,db_name)
- query_actions(connection_obj, query, query_type)

Example usage,

###### get_mysql_client

    from MrSnippets.mysql_wrapper import *
	conn = get_mysql_client('190.10.30.160', 'root', 'password', 'profile')

## SQL Wrapper

Its a collection of commonly used functions to minimize the code and time for SQL related operations.

#### List of supported functions,

- get_sql_client(server_ip,database,userName,pwd)
- query_actions(db_object, query, query_type)
- insert_records(connection_obj, table_data:dict, data_dict: dict, unique_columns:list)

Example usage,

###### sql_insert_records

    from MrSnippets.mysql_wrapper import *
    db_object = get_sql_client('195.16.40.82', 'SampleDB', 'root', 'password')
    sample_data = {'name':'dharan','phone_no':'023456789'}
    table_meta = {'db_name':'informationSystem','table_name':'contactInfo'}
    insert_records(db_object, table_data:dict, sample_data, ["phone_no"])

###### query_actions

    __author__ = 'dhamodharan.k'
    from MrSnippets.sql_wrapper import *
    db_object = get_sql_client('xx.xx.xx.xx', 'employeeData', 'root', 'pass')
    find_q = 'select emp_id,age from employee_info where emp_id in (4213958, 4213959)'
    rows = query_actions(db_object, find_q, 'select')
    for row in rows:
        content = str(row[1] + 1)
        update_query = "update employee_info set agePlus = '{}' where emp_id = {}".format(content,row[0])
        query_actions(db_object,update_query,'update')


## Prerequisites

Nothing but a basic knowlege of python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/dhamodharanrk/MrSnippets/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Dhamodharan** - (https://github.com/dhamodharanrk)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Required Libraries

###### Data Extraction
- beautifulsoup4>=4.3.3
- requests>=2.18.4
- html5lib>=1.0b10
- user_agent>=0.1.9
- selenium>= 3.141.0

###### Database

- PyMySQL>=0.9.3
- pymongo>=3.8.0

###### Text Pre-Processsing

- ftfy>=5.5.1
- tldextract>=2.2.1
- bleach>=3.1.0
- python-csv>=0.0.11

###### NLP Operations
- nltk>=3.4.5
- spacy>=2.3.2
- sklearn>=0.0

###### Utilities

- pytest-shutil>=1.6.0
- Pillow>=2.2.1
- pyodbc>=4.0.26
- fuzzywuzzy>=0.18.0
- pycountry>=19.8
- geopy>=1.21
- python-dateutil>=2.8.1
- urllib3>=1.25
- tldextract>=2.2.2
- geotext>=0.4.0
- dateparser>=1.0.0
- uuid>=1.30
- glob2>=0.7

# MrSnippets Change log

## Version 1.0.0
- Initial version with base features

## Version 1.0.1
- Included MySQL Wrappers with common functions
- Included Mongo Wrapper with common functions
- Improved function operations
- function documents are included

## Version 1.1.1
- Included Image Processing functions based on PIL and openCV
- fuzz Module removed (string compare function) which creating issue in installing the package
- all known bugs are fixed
- performance optimisations
- multiple methods are included for web_client
- more functions are added in helper module
- Added SQL wrapper
- Added missing library's in soup module

## Version 2.0.0
- Soup module renamed as data_mining module & Added many more functions
- Helper module renamed as utilities module & Added many more functions
- data converter module added which supports data conversion
- Added data_support Module with more data functions
- Now NLP module has more functionalities
- Included doc string for each and every functions
- Many Known bugs are fixed
- Document string added in all the functions
- Improved requirement file

## Acknowledgments

* Based on my experience am developing and including more functions to this package.
* In  upcoming days am planning to include as many functions as possible
* Any active contributors are welcome. Please free to reach out via email.
