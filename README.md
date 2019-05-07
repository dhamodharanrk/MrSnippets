# MrSelector
Its an simple implementation of css selector using Beautifulsoup. The selectors are stright forward and simple. 
It will defenetly reduce effortds to build effective scrapper.



There are list of pre-defined selector functions. For example selecting a single element from chunk as follows.

##### get_element(soup='',tag='',attributeName='',attributeValue='')


## List of fucntions supported now,

* get_element(soup, tag="div", attributeName='class', attributeValue='profile')

* get_elements(soup, tag="div", attributeName='class', attributeValue='profiles')

* find_sibling_text(soup, child:str, sibling:str, contains_string:str, sibling_type="prev|next")

* extract_hyper_link(soup_chunk,patterns:list,**kwargs)

* extract_vcard_link(soup_chunk,**kwargs)

* extract_image_link(soup_chunk,**kwargs)

* extract_vcard_data(vcard_text:str)
