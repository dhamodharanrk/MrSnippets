__author__ = 'dhamodharan.k'

from MrSnippets.helpers import *
from bs4 import BeautifulSoup

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
    # Extracting the profile url based on patterns found of profile url & returns list of dicts
    assert type(patterns) == list, "List require in Patterns"
    prefix = kwargs.get('prefix', '')
    with_text = kwargs.get('with_text', False)
    validate = lambda url: [1 for i in patterns if str(url).lower().__contains__(str(i).lower())]
    if with_text:
        if prefix: urls_found = [{"text":get_clean_text(link.text),"link":"{}{}".format(prefix,link["href"])} for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
        else: urls_found = [{"text":get_clean_text(link.text),"link":link["href"]} for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
    else:
        if prefix: urls_found = ["{}{}".format(prefix,link["href"]) for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
        else: urls_found = [link["href"] for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
    if urls_found: return urls_found
    else:
        if with_text: return [{'link':'','text':''}]
        else: return []

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

def extract_email_addresses(string):
    string = str(string)
    string = string.replace(' (at) ', '@')
    string = string.replace('(at)', '@')
    string = string.replace(' <at> ', '@')
    string = string.replace('<at>', '@')
    r = re.compile(r'[\w\-][\w\-\.]+[@]+[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
    return r.findall(string)

def extract_phone_numbers(html_chunk):
    number = None
    try:
        html_chunk = re.sub(r'&nbsp',':',str(html_chunk))
        pattern = re.compile( r'(\+?\d+(?:[- \\)]+\d+)+)')
        match = pattern.findall(html_chunk)
        match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el)) > 6]
        match = [re.sub(r'\D$', '', el).strip() for el in match]
        match = [el for el in match if len(re.sub(r'\D', '', el)) <= 15]
        try:
            for el in list(match):
                if len(el.split('-')) > 3 or len(el.split(' ')) > 3: continue
                for x in el.split("-"):
                    try:
                        if x.strip()[-4:].isdigit():
                            if int(x.strip()[-4:]) in range(1900, 2100):
                                match.remove(el)
                    except:pass
        except:pass
        number = match
    except: pass
    return number

def extract_social_links(self, html_source):
    patterns = ['facebook','twitter','linkedin','tumblr','instagram','skype','pinterest','youtube','flickr']
    validate = lambda url: [1 for i in patterns if str(url).lower().__contains__(str(i).lower())]
    urls_found = [link["href"] for link in html_source.find_all("a", href=True) if len(validate(link["href"])) > 0]
    return urls_found

def extract_meta_data(self, html_source):
    meta_chunks = html_source.find_all('meta')
    valid_meta = ['description', 'keywords']
    meta_data,meta = {"DG": 'meta'},[]
    for meta_tags in meta_chunks:
        content = meta_tags.get('content', '')
        name = meta_tags.get('name', '')
        if name in valid_meta: meta_data[name] = content
    meta.append(meta_data)
    return meta
