# This module extracts data from websites.

import os

import urllib.request

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
        data_returned = raw_data, was_redirected, final_url, http_code, success_flag
    else:
        data_returned = b'', was_redirected, final_url, error_code, success_flag
    
    return data_returned


aux = page_extractor(TEST_URL)
pass