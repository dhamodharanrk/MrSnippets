# MrSnippets

A collection of common codes or wrapper functions to simplify the coding time

## Getting Started

To get started install the package using below command on your machine.

`pip install MrSnippets`

Sample Usage,

    from MrSnippets.helpers import *
    print(get_numbers_from_string('1a2b3e'))

## Helper Module

Its an collection of commonly used functions to minimize the code and time.

- List of supported functions,
- get_clean_text(string:str)
- get_numbers_from_string(string:str)
- get_alpha_from_string(string:str)
- get_clean_list(list_x:list)
- get_clean_json_string(json_chunk,key)
- clean_dict(dict)
- get_string_from_html(soup)
- convert_base64_Image(encoded_data,path_to_store,file_name)

## Soup Wrapper

Its an simple implementation of css selector using Beautifulsoup. The selectors are stright forward and simple.

There are list of pre-defined selector functions. For example selecting a single element from chunk as follows.

`get_element(soup='',tag='',attributeName='',attributeValue='')`

#### List of fucntions supported now,

- get_element(soup, tag="div", attributeName='class', attributeValue='profile')
- get_elements(soup, tag="div", attributeName='class', attributeValue='profiles')
- find_sibling_text(soup, child:str, sibling:str, contains_string:str, sibling_type="prev|next")
- extract_hyper_link(soup_chunk,patterns:list,**kwargs)
- extract_vcard_link(soup_chunk,**kwargs)
- extract_image_link(soup_chunk,**kwargs)
- extract_vcard_data(vcard_text:str)

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
- list_database()
- list_collection(db:str)
- get_collection_summary(db:str,collection:str)
- get_sample_records(db:str,collection:str,query_by:str,value:str,limit:int=1)
- update_record(connection:dict,query_by:str,query_by_value,data:dict)

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

### Prerequisites

Nothing but a basic knowlege of python

## Contributing

Please read [CONTRIBUTING.md](https://github.com/dhamodharanrk/MrSnippets/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Dhamodharan** - (https://github.com/dhamodharanrk)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* It will be improved in near feature
