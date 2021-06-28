__author__ = 'dhamodharan.k'
import requests
import json
from MrSnippets.data_mining import extract_domain_name_from_url
from MrSnippets.utilities import *
from bs4 import BeautifulSoup
from itertools import cycle
from selenium import webdriver

def UPDATE_FETCHER_LOG(logDict):
    """
    the idea behind this is to store the logs in database.
    :param logDict: dict data
    :return: None
    """
    write_text_file('','request.log',str(logDict))

proxy_sets = {"xx.xx.xx.xxx:80", "xx.xx.xx.xxx:90"}
proxy_pool = cycle(proxy_sets)
def get_proxy():
    """
    :return: proxy dict
    """
    proxy = next(proxy_pool)
    return {"http": proxy, "https": proxy}

def get_selenium_response(url, timeout):
    """
    A method to get the selenium based response for the given URL
    :param url:  Input URL
    :param timeout: Max wait time for the request
    :return: BeautifulSoup object
    """
    browser = None
    if get_current_platform() == "windows":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('-headless')
        browser = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    # else:
        # os.environ["PATH"] += os.pathsep + BaseDir.fireFoxPath
        # options = webdriver.FirefoxOptions()
        # options.add_argument('-headless')
        # browser = webdriver.Firefox(executable_path=BaseDir.geckodriverPath, firefox_options=options,timeout=timeout)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    browser.close()
    browser.quit()
    return soup

def get_response(url, response_type, attempt=0, **kwargs):

    """
    A method used to get the web response and returns in user defined format.

    :param url: URL to get web response

    :param response_type: One of Pre-defined method to return the fetched response

        soup : Returns the web response as BeautifulSoup object

        text : Returns the web response as raw text

        json : returns the response as json object

        content : returns the web response as it is. Use full in fetching file objects

        response : returns the response code

    :param attempt: holds the number of retry should be performed

    :param kwargs: Holds multiple options to utilize the same method in multiple ways.

        data : Used in post method to provide data

        params : Used to pass parameters data for post method

        time_out : Used to set the timeout for the requests and its an integer

        verify : Verify the HTTP Certificate. Will be Bool value. By default True

        method : pre-defined value either POST or GET

        headers : dict data holds the HTTP headers. By default holds the User-Agent String

        allow_redirects : Bool value

        stream : Bool value

        request_type : Pre-defined value. Either requests or selenium

        dom_parser : method to parse HTML in BeautifulSoup. By default html5lib

    :return: returns as per response_type args


    """
    RESPONSE_DATA = None
    response = None
    data = kwargs.get('data', {})
    gateway = kwargs.get('gateway', 'requests')
    params = kwargs.get('params', {})
    timeout = kwargs.get('time_out', 60)
    verify = kwargs.get('verify', True)
    method = kwargs.get('method', None)
    domain = kwargs.get('domain', '')
    if not domain : domain = extract_domain_name_from_url(url)
    headers = kwargs.get('headers',{})
    allow_redirects = kwargs.get('allow_redirects', True)
    proxy =  kwargs.get('proxy', True)
    stream =  kwargs.get('stream', False)
    dom_parser = kwargs.get('dom_parser','html5lib')
    headers.update({'User-Agent': get_user_agent(domain_name=domain)})
    proxy = get_proxy() if proxy else {}
    try: currentIP = str(proxy['http']).split("@")[1]
    except: currentIP = ''
    if currentIP: print("[{}] : {}".format(currentIP,url))
    else: print("[{}] : {}".format("NO PROXY*",url))

    hashData = hashlib.md5(str(url).encode())
    URLMETA = {'IP':str(currentIP),"domain": domain,'rowkey':str(hashData.hexdigest()),"url": url,'timeStamp': str(datetime.now()),'LogType':'NA','User-Agent': headers.get('User-Agent','NA'),'Method': str(method).upper() if method else "GET",'Error':'NA'}

    REQUEST_META_LOG = {"ResponseType":response_type,'RequestData':json.dumps(kwargs)}
    URLMETA.update({"RequestMeta":REQUEST_META_LOG})
    try:
        if gateway == 'selenium':
            try:
                response = get_selenium_response(url, timeout)
            except Exception as error:
                response = None
                URLMETA.update({'log_type': 'Error', 'response_code': 'NA', 'retry': attempt, 'Error': str(error)})
        elif gateway == "requests":
            if str(method).upper() == 'POST':
                response = requests.post(url, data = data, params=params, headers=headers, proxies = proxy, timeout=timeout, verify=verify)
                response_status = response.status_code
                URLMETA.update({'log_type':'Request','response_code': str(response_status), 'retry': attempt})
            else:
                response = requests.get(url, data=data, params=params, headers=headers, proxies = proxy, timeout=timeout, verify=verify, allow_redirects=allow_redirects, stream=stream)
                response_status = response.status_code
                URLMETA.update({'log_type': 'Request','response_code': str(response_status), 'retry': attempt})
    except Exception as error:
        response = None
        if 'Caused by ProxyError' in str(error):
            URLMETA.update({'log_type': 'Error', 'response_code': 'NA', 'retry': attempt, 'Error': str(error)})
            print('Attempting with different Proxy! Proxy ' + proxy['http'] + ' has been identified by server!')
        else:
            print('Error occurred while fetching page response. Error Message -- ' + str(error) + str(url))
    if response:
        try:
            if response.status_code == 200 and gateway != "selenium":
                page_response = response
                if response_type == 'soup': RESPONSE_DATA = BeautifulSoup(page_response.text, dom_parser)
                elif response_type == 'text': RESPONSE_DATA = page_response.text
                elif response_type == 'content': RESPONSE_DATA = response.content
                elif response_type == 'json': RESPONSE_DATA = response.json()
                elif response_type == 'response': RESPONSE_DATA = response
            if response.status_code == 429 or response.status_code == 401 and gateway != "selenium":
                get_response(url, response_type, attempt + 1, **kwargs)
            elif gateway == "selenium":
                RESPONSE_DATA = response
            else:
                response_status = response.status_code
                URLMETA.update({'log_type': 'Error','response_code': str(response_status), 'retry': attempt})
        except Exception as e:
            URLMETA.update({'log_type': 'Error','response_code': 'NA', 'retry': attempt,'Error':str(e)})
    else:
        if attempt < 6:
            print('Attempt {attempt} : Empty response found for '.format(attempt=attempt) + currentIP + " ! Attempting with different Proxy..")
            get_response(url, response_type, attempt + 1, **kwargs)
    UPDATE_FETCHER_LOG(URLMETA)
    return RESPONSE_DATA


def download_file(url,dir,file_name,extension):
    """

    :param url: download link
    :param dir: directory to store the file
    :param file_name: file name for the download, Optional None
    :param extension: file extension without dot
    :return: None
    """

    if not os.path.exists(dir): os.makedirs(dir)
    try:
        response_obj = get_response(url,'response', proxy=True, stream=True)
        if response_obj:
            if not file_name:
                file_name = genearate_hash_key(str(url))
            with open(dir + file_name + "." + extension, 'wb') as f:
                for chunk in response_obj.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as ValueError:
        print(ValueError)