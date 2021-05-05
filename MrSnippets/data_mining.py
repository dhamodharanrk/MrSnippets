__author__ = 'dhamodharan.k'
from MrSnippets.helpers import *
import dateparser
import pycountry
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="MrSnippets")
from dateutil import parser
from urllib.parse import urlparse
import tldextract


############################## HTML Functions ##############################

def get_element(soup, tag="div", attributeName='class', attributeValue='profile'):
    """
    :param soup: HTML Bs4 object
    :param tag: tag needs to be extracted. Example Div
    :param attributeName: variable name. Example class
    :param attributeValue: example "profile" . class="profile"
    :return: subset of html element
    """
    try:
        html_tag = soup.find(tag, {attributeName: attributeValue})
    except:
        return None
    return html_tag

def get_elements(soup, tag="div", attributeName='class', attributeValue='profiles'):
    """
    :param soup:
    :param tag:
    :param attributeName:
    :param attributeValue:
    :return:
    """
    try:
        html_tags = soup.findAll(tag, {attributeName: attributeValue})
    except:
        return None
    return html_tags

def get_element_by_tag(soup,selector_string:str):
    """

    :param soup:
    :param selector_string:
    :return:
    """
    try:
        element = BeautifulSoup(selector_string,'html5lib').body.next
        return soup.find(element.name,element.attrs)
    except: return None

def get_elements_by_tag(soup,selector_string:str):
    """

    :param soup:
    :param selector_string:
    :return:
    """
    try:
        element = BeautifulSoup(selector_string,'html5lib').body.next
        return soup.find_all(element.name,element.attrs)
    except: return None

def get_sibling_text(soup, child: str, sibling: str, contains_string: str, sibling_type="prev|next"):
    """

    :param soup:
    :param child:
    :param sibling:
    :param contains_string:
    :param sibling_type:
    :return:
    """
    result = soup.find(child, string=contains_string)
    if sibling_type == 'next':
        text = result.findNext(sibling).text
    elif sibling_type == 'prev':
        text = result.findPrevious(sibling).text
    else:
        text = None
    return text

############################## Semi automated extration methods ##############################

def extract_hyper_link(soup_chunk, patterns: list, **kwargs):
    """
    Extracting the profile url based on patterns found of profile url & returns list of dicts
    :param soup_chunk:
    :param patterns:
    :param kwargs:
    :return:
    """
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
    """

    :param soup_chunk:
    :param kwargs:
    :return:
    """
    patterns = kwargs.get('patterns', ['.vcf', 'vcard'])
    prefix = kwargs.get('prefix', '')
    validate = lambda url: [1 for i in patterns if str(url).lower().__contains__(str(i).lower())]
    if prefix:
        urls_found = ["{}{}".format(prefix, link["href"]) for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
    else:
        urls_found = [link["href"] for link in soup_chunk.find_all("a", href=True) if len(validate(link["href"])) > 0]
    return urls_found

def extract_image_link(soup_chunk, **kwargs):
    """

    :param soup_chunk:
    :param kwargs:
    :return:
    """
    patterns = kwargs.get('patterns', ['media', 'images', 'image'])
    prefix = kwargs.get('prefix', '')
    validate = lambda url: [1 for i in patterns if str(url).lower().__contains__(str(i).lower())]
    if prefix:
        urls_found = ["{}{}".format(prefix, link["src"]) for link in soup_chunk.find_all("img", src=True) if len(validate(link["src"])) > 0]
    else:
        urls_found = [link["src"] for link in soup_chunk.find_all("img", src=True) if len(validate(link["src"])) > 0]
    return urls_found

def extract_vcard_data(vcard_text: str):
    """

    :param vcard_text:
    :return:
    """
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
    """

    :param string:
    :return:
    """
    string = str(string)
    string = string.replace(' (at) ', '@')
    string = string.replace('(at)', '@')
    string = string.replace(' <at> ', '@')
    string = string.replace('<at>', '@')
    r = re.compile(r'[\w\-][\w\-\.]+[@]+[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
    return r.findall(string)

def extract_phone_numbers(html_chunk):
    """

    :param html_chunk:
    :return:
    """
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

def extract_social_links(html_source):
    """

    :param self:
    :param html_source:
    :return:
    """
    patterns = ['facebook','twitter','linkedin','tumblr','instagram','skype','pinterest','youtube','flickr']
    validate = lambda url: [1 for i in patterns if str(url).lower().__contains__(str(i).lower())]
    urls_found = [link["href"] for link in html_source.find_all("a", href=True) if len(validate(link["href"])) > 0]
    return urls_found

def extract_meta_data(html_source):
    """

    :param self:
    :param html_source:
    :return:
    """
    meta_chunks = html_source.find_all('meta')
    valid_meta = ['description', 'keywords']
    meta_data,meta = {"DG": 'meta'},[]
    for meta_tags in meta_chunks:
        content = meta_tags.get('content', '')
        name = meta_tags.get('name', '')
        if name in valid_meta: meta_data[name] = content
    meta.append(meta_data)
    return meta

def extract_date_from_string(date_string: str):
    '''
    A method used to extract the date from any given date string.
    :param date_string: A string having date information
    :return: returns the extracted date in YYYY-MM-DD format
    '''
    correct_date = None
    try:
        t = dateparser.parse(date_string)
        correct_date = t.strftime("%Y-%m-%d")
    except:
        pass
    if not correct_date:
        try:
            t = parser.parse(date_string)
            correct_date = t.strftime("%Y-%m-%d")
        except:
            pass
    if not correct_date:
        try:
            t = parser.parse(date_string, fuzzy_with_tokens=True)
            if t: correct_date = t[0].strftime("%Y-%m-%d")
        except:
            pass
    return correct_date


def extract_countries_from_text(input_text):
    '''
    A method used to find the country mentions in given string
    :param input_text: Any text
    :return: country name in list
    '''
    countries = [country.name for country in pycountry.countries if
                 str(input_text).lower().__contains__(str(country.name).lower())]
    countries = countries if countries else None
    if not countries:
        location = geolocator.geocode(str(input_text))
        address = location.address
        countries = [country.name for country in pycountry.countries if
                     str(address).lower().__contains__(str(country.name).lower())]
    return countries

def extract_url_prefix(url_string: str):
    '''
    Returns the URL prefix value as string
    :param url_string: input url
    :return: URL prefix
    '''
    m = re.search('https?://([A-Za-z_0-9.-]+).*', str(url_string))
    prefix = str(url_string).split("/")[0] + "//" + m.group(1)
    return prefix

def extract_domain_name_from_url(url):
    if "http" in str(url) or "www" in str(url):
        parsed = tldextract.extract(url)
        parsed = ".".join([i for i in parsed if i])
        return parsed
    else: return "NA"

############################## Support Functions ##############################

def get_parsed_url(url_string):
    return urlparse(url_string)

def validate_url(url):
    '''
    A method to validate the given URL string for URL schema

    :param url: input url string

    :return: returns bool value if conditions are met
    '''
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, str(url))

def fix_url_format(self, url, prefix):
    """

    A method used to fix the URL related issues in the data extraction process. As of now it will support following formation issues.

        "/pipeline/archives/2020/04/22/the-politics-of-hydroxychloroquine",
        "pipeline/archives/2020/04/22/the-politics-of-hydroxychloroquine",
        "http://google.com/pipeline/archives/2020/04/22/the-politics-of-hydroxychloroquine",
        "https://google.com/pipeline/archives/2020/04/22/the-politics-of-hydroxychloroquine",
        "//www.google.com/pipeline/archives/2020/04/22/the-politics-of-hydroxychloroquine",
        "www.google.com/pipeline/archives/2020/04/22/the-politics-of-hydroxychloroquine",
        "www.google.com/pipeline/archives/2020/04/22/the-politics-of-hydroxychloroquine",

    :param url: String input

    :param prefix: Base URL string like https://google.com

    :return: updated URL
    """

    fixed_url = url
    url = url[1:] if str(url).startswith("/") else url
    url = url[1:] if str(url).startswith("/") else url
    domain_name = self.extract_domain_name(prefix)
    url_schema = "https" if str(prefix).__contains__('https') else "http"
    if not self.validate_url(url):
        url = "{}/{}".format(domain_name, url) if not str(url).__contains__(domain_name) else url
        if url.startswith('http://www.'):
            fixed_url = 'http://' + url[len('http://www.'):]
        if url.startswith('https://www.'):
            fixed_url = 'https://' + url[len('https://www.'):]
        if url.startswith('www.'):
            fixed_url = '{}://'.format(url_schema) + url[len('www.'):]
        if not url.startswith("http"):
            fixed_url = "http://{}".format(url)
    return fixed_url

############################## Data Manipulations ##############################

def get_standard_name(name:str):
    """
    :param name: takes name strings
    :return: returns the name in standard format
    """
    reobj = re.compile(r'(?sm)((Dr|Ph\.D|Jr|LL\.M|Avv|\b[A-Z]{1}|\b[a-z]{1}|Prof)\.|\b(Dr|Jr|Ph\.D|LL\.M|PhD|LLM|Dipl.-Jur.|Jur|DAPI|\*|,\s*[A-Z]{2,4}|[A-Z]{1})(\s|$)|\(.*?\)|(".*?")|(/|;).*?$)')
    match = reobj.search(name)
    if match:
        refined_name = re.sub(r'(?sm)((Dr|Ph\.D|Jr|LL\.M|\b[A-Z]{1}|\b[a-z]{1}|Prof)\.|\b(Dr|Jr|Ph\.D|LL\.M|PhD|LLM|Dipl.-Jur.|Jur|DAPI|\*|,\s*[A-Z]{2,4}|[A-Z]{1})(\s|$)|\(.*?\)|(".*?")|(/|;).*?$)', '', name)
        refined_name = refined_name.replace('  ', ' ').strip()
    else: refined_name = get_clean_text(name)
    return refined_name

def split_name(name_string:str,reverse_it:bool=False,**kwargs):
    """
    :param name_string: takes the name as string
    :param reverse_it: accepts bool value. 1, revers the last name, first name else first name, last name
    :param kwargs: delimiter, delimiter value between first name, last name
    :return:
    """
    split_by = kwargs.get('delimiter'," ")
    assert len(name_string.split(split_by)) > 1, "Given String is not splittable by given delimiter key"
    nameData = {}
    name = ftfy.fix_text(refine_name(name_string))
    name_split = str(name).split(split_by)
    if reverse_it:
        name_split = list(reversed(name_split))
        name = " ".join(name_split)
    fname,lname = name_split[0],name_split[-1]
    nameData['FullName'] = name
    nameData['FirstName'] = fname
    nameData['LastName'] = lname
    return nameData