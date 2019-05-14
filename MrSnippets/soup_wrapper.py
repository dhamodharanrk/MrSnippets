__author__ = 'dhamodharan.k'

from MrSnippets.helpers import *

'''Implementation of CSS Wrapper functions'''

#===============Soup Functions=====================

def get_element(soup, tag="div", attributeName='class', attributeValue='profile'):
    try:
        html_tag = soup.find(tag, {attributeName: attributeValue})
    except:
        return None
    return html_tag

def get_elements(soup, tag="div", attributeName='class', attributeValue='profiles'):
    try:
        html_tags = soup.findAll(tag, {attributeName: attributeValue})
    except:
        return None
    return html_tags

def get_element_by_tag(soup,selector_string:str):
    try:
        element = BeautifulSoup(selector_string,'html5lib').body.next
        return soup.find(element.name,element.attrs)
    except: return None

def get_elements_by_tag(soup,selector_string:str):
    try:
        element = BeautifulSoup(selector_string,'html5lib').body.next
        return soup.find_all(element.name,element.attrs)
    except: return None

def get_sibling_text(soup, child: str, sibling: str, contains_string: str, sibling_type="prev|next"):
    result = soup.find(child, string=contains_string)
    if sibling_type == 'next':
        text = result.findNext(sibling).text
    elif sibling_type == 'prev':
        text = result.findPrevious(sibling).text
    else:
        text = None
    return text

# Semi Automated Process
def extract_hyper_link(soup_chunk, patterns: list, **kwargs):
    prefix = kwargs.get('prefix', '')
    urls_found = []
    with_text = kwargs.get('with_text', False)
    validate = lambda url: [1 for i in patterns if str(url).lower().__contains__(str(i).lower())]
    if with_text:
        if prefix:
            urls_found = [{"text": get_clean_text(link.text), "link": "{}{}".format(prefix, link["href"])} for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
        else:
            urls_found = [{"text": get_clean_text(link.text), "link": link["href"]} for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
    else:
        if prefix:
            urls_found = ["{}{}".format(prefix, link["href"]) for link in soup_chunk.find_all("a", href=True) if
                          len(validate(link["href"])) > 0]
        else:
            urls_found = [link["href"] for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
    return urls_found

def extract_vcard_link(soup_chunk, **kwargs):
    patterns = kwargs.get('patterns', ['.vcf', 'vcard'])
    prefix = kwargs.get('prefix', '')
    validate = lambda url: [1 for i in patterns if str(url).lower().__contains__(str(i).lower())]
    if prefix:
        urls_found = ["{}{}".format(prefix, link["href"]) for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
    else:
        urls_found = [link["href"] for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
    return urls_found

def extract_image_link(soup_chunk, **kwargs):
    patterns = kwargs.get('patterns', ['media', 'images', 'image'])
    prefix = kwargs.get('prefix', '')
    validate = lambda url: [1 for i in patterns if str(url).lower().__contains__(str(i).lower())]
    if prefix:
        urls_found = ["{}{}".format(prefix, link["src"]) for link in soup_chunk.find_all("img", src=True) if len(validate(link["src"])) > 0]
    else:
        urls_found = [link["src"] for link in soup_chunk.find_all("img", src=True) if len(validate(link["src"])) > 0]
    return urls_found

def extract_vcard_data(vcard_text: str):
    extracted = {}
    try:
        contents = vcard_text.splitlines()
        tel = [i for i in contents if 'TEL;WORK;VOICE' in str(i)]
        if not tel: tel = [i for i in contents if 'TEL;type=WORK,voice:' in str(i)]
        extracted['Tel'] = tel[0].split(':')[-1] if tel else ''
        email = [i for i in contents if 'EMAIL;PREF;INTERNET' in str(i)]
        if not email:
            email = [i for i in contents if 'EMAIL;TYPE=internet,pref' in str(i)]
        elif not email:
            email = [i for i in contents if 'EMAIL;type=INTERNET,pref' in str(i)]
        extracted['Email'] = email[0].split(':')[-1] if email else ''
        address = [i for i in contents if 'ADR' in str(i)]
        extracted['Location'] = address[0].split(';')[-4]
        return extracted
    except:
        return {}


def extract_social_links(self, html_source):
    pass

def extract_meta_data(self, html_source):
    pass
