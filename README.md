# MrSnippets

A complete collection of common code snippets

## Getting Started

To get started install the package using below command on your machine.

`pip install MrSnippets`

Sample Usage,

    from MrSnippets.helpers import *
    print(get_numbers_from_string('1a2b3e'))

## Helper Module

Its an collection of commonly used functions to minimize the code and time.

#### List of supported functions,
- get_clean_text(string:str)
- get_numbers_from_string(string:str)
- get_alpha_from_string(string:str)
- get_string_from_html(soup)
- join_string(source_list:list, separator:str='')
- compare_string(string_one,string_two)
- get_clean_list(list_x:list)
- compare_list(first:list, second:list)
- find_list_duplicates(list:list)
- get_clean_dict(dict:dict)
- modify_jsondata(abbreviations_dict:dict,target_dict:dict)
- refine_name(name:str)
- split_name(name_string:str,reverse_it:bool=False,**kwargs)


## Soup Wrapper

Its an simple implementation of css selector using Beautifulsoup. The selectors are stright forward and simple.

There are list of pre-defined selector functions. For example selecting a single element from chunk as follows.

    from MrSnippets.soup_wrapper import  *
    name = get_element(html_chunk,'div','class','people_name')
    name = get_element_by_tag(html_chunk,'<div class="people_name">')


#### List of fucntions supported now,

- get_element(soup, tag="div", attributeName='class', attributeValue='profile')
- get_elements(soup, tag="div", attributeName='class', attributeValue='profiles')
- get_element_by_tag(soup,selector_string:str)
- get_elements_by_tag(soup,selector_string:str)
- get_sibling_text(soup, child:str, sibling:str, contains_string:str, sibling_type="prev|next")
- extract_hyper_link(soup_chunk,patterns:list,**kwargs)
- extract_social_links(self, html_source)
- extract_vcard_link(soup_chunk,**kwargs)
- extract_image_link(soup_chunk,**kwargs)
- extract_vcard_data(vcard_text:str)
- extract_meta_data(self, html_source)
- extract_email_addresses(string)
- extract_phone_numbers(html_chunk)

## Mongo Wrapper
Its an collection of commonly used functions to minimize the code and time for mongo related operations.

To Setup the Client IP do follow the below steps,

Enter Below piece of code

1. **from MrSnippets.mongo_wrapper import MONGO_CLIENT_IP**
2. Now, **CTRL + Right Click** on **MONGO_CLIENT_IP**
3. Update this *'xx.xx.xx.xxx'* to Your IP (195.16.20.335:27017)

`MONGO_CLIENT_IP = 'xx.xx.xx.xxx:27017'`

post update we will something like this,

`MONGO_CLIENT_IP = '195.16.20.335:27017'`

#### List of fucntions supported now,

- get_mongo_client(database_name, collection_name)
- list_db()
- list_collections(db:str)
- get_summarize(db:str,collection:str)
- get_sample(db:str,collection:str,query_by:str,value:str,limit:int=1)
- update_record(connection:dict,query_by:str,query_by_value,data:dict)
- create_index(connection:dict,index_attributes:list,ascending:bool=True)
- update_attribute(connection:dict,query_by:str,query_by_value,data:dict,attributes:list)

## MySQL Wrapper

Its an collection of commonly used functions to minimize the code and time for MySQL related operations.

#### List of fucntions supported now,

- get_mysql_client(host_ip, username, pwd,db_name)
- query_actions(connection_obj, query, query_type)

Example usage,

###### get_mysql_client

    from MrSnippets.mysql_wrapper import *
	conn = get_mysql_client('190.10.30.160', 'root', 'password', 'profile')

## SQL Wrapper

Its an collection of commonly used functions to minimize the code and time for SQL related operations.

#### List of fucntions supported now,

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

## Web Client

Its an collection of commonly used function for inracting on Internet

#### List of fucntions supported now,

- get_user_agent(**kwargs)
- extract_domain_name(url)
- downloader(url,dir,file_name,extension)
- get_response(url, response_type, attempt=0, **kwargs)

available  arguments  for this function

    data = kwargs.get('data',{})
	params = kwargs.get('params',{})
    timeout = kwargs.get('time_out', 60)
    verify = kwargs.get('verify', True)
    method = kwargs.get('method', None)
    domain = kwargs.get('domain', '')
    headers = kwargs.get('headers',{})
    allow_redirects = kwargs.get('allow_redirects', True)
    proxy =  kwargs.get('proxy', True)
    stream =  kwargs.get('stream', False)
    dom_parser = kwargs.get('dom_parser','html5lib')

Sample Usage:

    response = get_response(url,'json',method='post', data = payload, headers=headers, timeout=100, verify=False)

## Natural Language Processing

Collection of  functions to minimize the code and time for NLP related operations.

#### List of fucntions supported now,

- clean_my_html(html_source)
- get_top_keywords(self, html_source)
- get_word_frequency(html_source, search_words)
- get_tokenized(string:str,ignore_stopwords:bool=False)
- get_lemmatize_data(tokens:list)
- get_standardize_words(tokens:list,lookup_dict:dict)
- generate_ngrams(tokens:list,n)

```python
search_words = ['programmer','dhamodharanrk']
frequency = get_word_frequency(html_source, search_words)
search_words = {'name': 'john,ram', 'brand': 'apple,nokia,samsung'}
frequency = get_word_frequency(html_source, search_words)
lookup_dict = {'rt':'Retweet', 'dm':'direct message', "awsm" : "awesome", "luv" :"love"}
standardize_words = get_standardize_words(tokens,lookup_dict )
```

## Image Processing

Collection of  functions to minimize the code and time for image processing tasks

#### List of fucntions supported now,
- adjust_brightness(input_image, output_image, factor)
- adjust_contrast(input_image, output_image, factor)
- adjust_sharpness(input_image, output_image, factor)
- resize_image(input_image_path,output_image_path,size)
- scale_image(input_image_path,output_image_path,width=None,height=None)
- black_and_white(input_image_path,output_image_path)
- rotateImage(image_path, degrees_to_rotate, saved_location)
- flipImage(image_path, saved_location,direction)
- cropImage(image_path, coords, saved_location)

## Misc Functions

Collection of  functions to minimize the code and time for day to day tasks

#### List of fucntions supported now,

- read_text_file(file_name)
- write_text_file(filepath, filename, content)
- write_csv_file(filepath,filename,content:dict,headers:list)
- get_base64Image(encoded_data,path_to_store,file_name)
- get_city_list()
- get_state_list()
- get_city_info_obj()
- get_sizeof(num, suffix='o')
- get_current_user()
- get_parsed_url(url_to_parse)
- get_filename(file_name)
- move_to(source,destination,filename)
- copy_to(source,destination,filename)
- list_files(diretory,ext:str='')


### Prerequisites

Nothing but a basic knowlege of python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/dhamodharanrk/MrSnippets/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Dhamodharan** - (https://github.com/dhamodharanrk)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Required Libraries
- beautifulsoup4>=4.3.3
- PyMySQL>=0.9.3
- pymongo>=3.8.0
- user_agent>=0.1.9
- ftfy>=5.5.1
- tldextract>=2.2.1
- bleach>=3.1.0
- python-csv>=0.0.11
- requests>=2.18.4
- html5lib>=1.0b10
- pytest-shutil>=1.6.0
- Pillow>=2.2.1
- pyodbc>=4.0.26

## Acknowledgments

* This module has been actively developed.
* More and more features will be realised on upcomming days.
* This entire code is based on my experiance and scenarios crossed.   Door open for any suggestions.
* Active contributors are welcome