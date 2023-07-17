# This module extracts data from websites. It also parses it by text and links.

import os

import urllib.request
from bs4 import BeautifulSoup


TEST_URL = 'https://en.wikipedia.org/wiki/Main_Page'
#TEST_URL = 'https://eaa'

search_url = TEST_URL

# EXTRACTION
def page_extractor(search_url):
    success_flag = True
    data_returned = []
    was_redirected = False

    final_url = ''
    http_code = 0
    error_code = 0

    try: # Gets the url
        with urllib.request.urlopen(search_url, timeout = 20.0) as response:
            raw_data = response.read()
        final_url = response.url # Gets the final page, if redirected
        http_code = response.status

        if final_url != search_url: # This means there was a redirection
            was_redirected = True

    except urllib.error.URLError as e: # Unable to access URL
        success_flag = False
        if e.reason.errno == 11001:
            # Unable to connect. Possible connection error or wrong URL
            error_code = e.reason.errno
        else:
            # This can be any error code, like '403', '404'...
            error_code = e.code

    if success_flag:
        data_returned = (raw_data,
                         was_redirected,
                         final_url,
                         http_code,
                         success_flag)
    else:
        data_returned = (b'',
                         was_redirected,
                         final_url,
                         error_code,
                         success_flag)
    
    return data_returned

# PARSING
# URLs
def parse_urls(raw_data):
    # Returns all URLs from a page's raw data
    url_soup = BeautifulSoup(raw_data, 'html.parser')
    aux = url_soup.find_all('a')
    link_list = []
    for item in aux:
        ref = item.get('href')
        if ref != None and (ref.startswith('http') or ref.startswith('www')):
            link_list.append(ref)

    # Remove URLs containing dangerous characters
    # Turns out some URLs really confuse Python
    # due to them containing special characters such as '\'
    dangerous_chars = ['\'', '\"', '\\']
    clean_list = []
    for link in link_list:
        is_present = any(char in link for char in dangerous_chars)
        if not is_present:
            clean_list.append(link)

    return clean_list

# TEXT
def parse_text(raw_data):
    text_soup = BeautifulSoup(raw_data, 'html.parser')
    text = text_soup.get_text()

    text = text.split('\n') # Split into lines
    text = [x.replace('\t', '') for x in text] # Remove '\t'
    text = [x for x in text if x != ''] # Remove empty elements

    return text


data_package = page_extractor(TEST_URL)
url_list = parse_urls(data_package[0])
text_list = parse_text(data_package[0])


pass