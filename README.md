# MrSnippets

A collection of common codes or wrapper functions to simplify the coding time

## Getting Started

To get started install the package using below command on your machine.

`pip install MrSnippets`

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

## Soup Module

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
