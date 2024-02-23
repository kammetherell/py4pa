import urllib3
urllib3.disable_warnings()
from fake_useragent import UserAgent

def get_random_useragent(browser=None):
    '''Function to generate a random user agent for web scraping

    Parameters
    ----------
    browser: String
        Valid values are: 'ie', 'opera', 'chrome', 'firefox', 'safari'

    Returns
    ----------
    String of valid User Agent

    '''

    ua = UserAgent()

    useragent = ua.random

    if browser is not None:
        useragent = ua[browser]

    return useragent


