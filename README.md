# MrSnippets

A complete collection of common codes

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
- extract_vcard_link(soup_chunk,**kwargs)
- extract_image_link(soup_chunk,**kwargs)
- extract_vcard_data(vcard_text:str)
- extract_social_links(self, html_source)
- extract_meta_data(self, html_source)

## Mongo Wrapper
Its an collection of commonly used functions to minimize the code and time for mongo related operations.

To Setup the Client IP do follow the below steps,

Enter Below piece of code

1. **from MrSnippets.mongo_wrapper import MONGO_CLIENT_IP**
2. Now, **CTRL + Right Click** on **MONGO_CLIENT_IP**
3. Update this *'xx.xx.xx.xxx'* to Your IP (10.10.20.335:27017)

`MONGO_CLIENT_IP = 'xx.xx.xx.xxx:27017'`

post update we will something like this,

`MONGO_CLIENT_IP = '10.10.20.335:27017'`

#### List of fucntions supported now,

- get_mongo_client(database_name, collection_name)
- mongo_dbs()
- mongo_collections(db:str)
- mongo_summarize(db:str,collection:str)
- mongo_sample(db:str,collection:str,query_by:str,value:str,limit:int=1)
- mongo_update_record(connection:dict,query_by:str,query_by_value,data:dict)
- mongo_create_index(connection:dict,index_attributes:list,ascending:bool=True)

## MySQL Wrapper

Its an collection of commonly used functions to minimize the code and time for MySQL related operations.

#### List of fucntions supported now,

- get_mysql_client(host_ip, username, pwd,db_name)
- execute_mysql_query(connection, query)

Example usage,

###### execute_mysql_query

    from MrSnippets.mysql_wrapper import *
	conn = get_mysql_client('10.10.10.223', 'root', 'password', 'profile')
    query = 'select * from sample;'
    result_rows = mysql_action(conn, query)

## Web Client

Its an collection of commonly used function for inracting on Internet

#### List of fucntions supported now,

- get_user_agent(**kwargs)
- extract_domain_name(url)
- downloader(url,dir,file_name,extension)
- get_response(url, response_type, attempt=0, **kwargs)

available  arguments  for this function

    payload = kwargs.get('payload',{})
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

    response = get_response(url,'json',method='post', payload = data, headers=headers, timeout=100, verify=False)

## Natural Language Processing

Collection of  functions to minimize the code and time for NLP related operations.

#### List of fucntions supported now,

- clean_my_html(html_source)
- get_top_keywords(self, html_source)
- get_word_frequency(html_source, search_words)


    search_words = ['programmer','dhamodharanrk']
    frequency = get_word_frequency(html_source, search_words)
    search_words = {'name': 'john,ram', 'brand': 'apple,nokia,samsung'}
    frequency = get_word_frequency(html_source, search_words)

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

### Prerequisites

Nothing but a basic knowlege of python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/dhamodharanrk/MrSnippets/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Dhamodharan** - (https://github.com/dhamodharanrk)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Required Libraries

- beautifulsoup4>=4.7.1
- PyMySQL>=0.9.3
- pymongo>=3.8.0
- user_agent>=0.1.9
- ftfy>=5.5.1
- tldextract>=2.2.1
- bleach>=3.1.0
- python-csv>=0.0.11

## Acknowledgments

* This module has been actively developed.
* More and more features will be realised on upcomming days.
* This entire code is based on my experiance and scenarios crossed.   Door open for any suggestions.
* Active contributors are welcome
