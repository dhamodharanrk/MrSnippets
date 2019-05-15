__author__ = 'dhamodharan.k'
from user_agent import generate_user_agent
import tldextract
import os
import requests
from datetime import datetime
import hashlib
import json
from bs4 import BeautifulSoup
from MrSnippets.misc import *
from itertools import cycle


def UPDATE_FETCHER_LOG(logDict):
    # Idea behind is to store on DB. Currently structured for mongo
    write_text_file('','request.log',str(logDict))

def get_user_agent(**kwargs):
    domain_specific = {}
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    try:
        domain_name = kwargs.get('domain_name','NA')
        user_agent = domain_specific.get(domain_name) if domain_name in domain_specific.keys() else generate_user_agent(device_type='desktop',os=['win','linux','mac'])
    except: pass
    return user_agent

def extract_domain_name(url):
    if "http" in str(url) or "www" in str(url):
        parsed = tldextract.extract(url)
        parsed = ".".join([i for i in parsed if i])
        return parsed
    else: return "NA"

def downloader(url,dir,file_name,extension):
    if not os.path.exists(dir): os.makedirs(dir)
    try:
        response_obj = get_response(url,'response', proxy=True, stream=True)
        if response_obj:
            with open(dir + file_name + "." + extension, 'wb') as f:
                for chunk in response_obj.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as ValueError:
        print(ValueError)

# Its a sample implementation, In real life scanario it won't work as expected since this module initialized each time while calling it.
# To overcome and keep all track of proxies, i choose my own algorithm
# Using random function is better option but it won't help in-terms of sequence hits

proxy_sets = {"xx.xx.xx.xxx:80", "xx.xx.xx.xxx:90"}
proxy_pool = cycle(proxy_sets)
def get_proxy():
    proxy = next(proxy_pool)
    return {"http": proxy, "https": proxy}
#End

def get_response(url, response_type, attempt=0, **kwargs):
    RESPONSE_DATA = None
    payload = kwargs.get('payload', 60)
    timeout = kwargs.get('time_out', 60)
    verify = kwargs.get('verify', True)
    method = kwargs.get('method', None)
    domain = kwargs.get('domain', '')
    if not domain : domain = tldextract.extract(url).domain
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
        if str(method).upper() == 'POST':
            response = requests.post(url, data = payload, headers=headers, proxies = proxy, timeout=timeout, verify=verify)
            response_status = response.status_code
            URLMETA.update({'log_type':'Request','response_code': str(response_status), 'retry': attempt})
        else:
            response = requests.get(url, data = payload, headers=headers, proxies = proxy, timeout=timeout, verify=verify, allow_redirects=allow_redirects, stream=stream)
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
            if response.status_code == 200:
                page_response = response
                if response_type == 'soup': RESPONSE_DATA = BeautifulSoup(page_response.text, dom_parser)
                elif response_type == 'text': RESPONSE_DATA = page_response.text
                elif response_type == 'content': RESPONSE_DATA = response.content
                elif response_type == 'json': RESPONSE_DATA = response.json()
                elif response_type == 'response': RESPONSE_DATA = response
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