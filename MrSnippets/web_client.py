__author__ = 'dhamodharan.k'
from user_agent import generate_user_agent
import tldextract

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