# This module extracts data from websites. It also parses it by text and links.

import os

import urllib.request
from bs4 import BeautifulSoup

import urllib.parse as urlparse

# EXTRACTION
def page_extractor(search_url):
    success_flag = True
    data_returned = []
    was_redirected = False

    final_url = ''
    http_code = 0
    error_code = 0

    # Treats URLs with special characters
    search_url = urllib.parse.quote(sanitize_url_to_name(search_url))
    search_url = 'http://' + search_url

    try: # Gets the url
        with urllib.request.urlopen(search_url, timeout = 20.0) as response:
            raw_data = response.read()
        final_url = response.url # Gets the final page, if redirected
        http_code = response.status

        if final_url != search_url: # This means there was a redirection
            was_redirected = True

    except:
        success_flag = False
        error_code = '?'
        print('UNKNOWN ERROR')
            

    if success_flag:
        data_returned = (raw_data,
                         was_redirected,
                         search_url,
                         final_url,
                         http_code,
                         success_flag)
    else:
        data_returned = (b'',
                         was_redirected,
                         search_url,
                         final_url,
                         error_code,
                         success_flag)
    
    return data_returned

# PARSING
# URLs
def parse_urls(raw_data):
    # Returns all URLs from a page's raw data
    try:
        url_soup = BeautifulSoup(raw_data, 'html.parser')
    except:
        print('URL Parser Error: Unable to parse URLs')
        return []
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
    try:
        text_soup = BeautifulSoup(raw_data, 'html.parser')
    except:
        print('Text Parser Error: Unable to parse text')
        return []
    text = text_soup.get_text()

    text = text.split('\n') # Split into lines
    text = [x.replace('\t', '') for x in text] # Remove '\t'
    text = [x for x in text if x != ''] # Remove empty elements

    return text

# WEBSITE NAME
def sanitize_url_to_name(input):
   removal_list = ['http://', 'https://', 'www.']
   
   output = input
   for item in removal_list:
      output = output.replace(item, '')
   
   if output[-1] == '/':
      output = output[:-1]

   return output

# Illegal characters for filesystem and substitutes
illegal_filename_characters = ['#', '<', '$', '+', '%','>', '!', '`', '&', '*', "'", '|', '{', '?', '"', '=', '}', ':', '\\', '\xa0', '@', ';']
translation_characters = ['☺', '☻', '♥', '♦', '♣', '♠', '•', '○', '◙', '♂', '♀', '♪', '♫', '☼', '►', '◄', '↕', '‼', '¶', '§', '▬', '↨']
def sanitize_url_to_filesystem_name(input):
   mode = 0
   input = sanitize_url_to_name(input)
   global illegal_filename_characters
   global translation_characters

   if mode == 0: # URL to filesystem
      for i in range(len(illegal_filename_characters)):               
         input = input.replace(illegal_filename_characters[i], translation_characters[i])
   else:
      # TODO Translate back
      pass

   return input

# CONVERSION AND STUFF
def iri_to_uri(iri, encoding='Latin-1'):
    "Takes a Unicode string that can contain an IRI and emits a URI."
    scheme, authority, path, query, frag = urlparse.urlsplit(iri)
    scheme = scheme.encode(encoding)
    if ":" in authority:
        host, port = authority.split(":", 1)
        authority = host.encode('idna') + ":%s" % port
    else:
        authority = authority.encode(encoding)
    path = urllib.quote(
      path.encode(encoding), 
      safe="/;%[]=:$&()+,!?*@'~"
    )
    query = urllib.quote(
      query.encode(encoding), 
      safe="/;%[]=:$&()+,!?*@'~"
    )
    frag = urllib.quote(
      frag.encode(encoding), 
      safe="/;%[]=:$&()+,!?*@'~"
    )
    return urlparse.urlunsplit((scheme, authority, path, query, frag))

# GET FULL DATA
def get_data_from_url(search_url):
    (raw_data,
     was_redirected,
     search_url,
     final_url,
     http_code,
     success_flag) = page_extractor(search_url)
    
    website_name = sanitize_url_to_filesystem_name(search_url)
    
    url_list = parse_urls(raw_data)
    text_list = parse_text(raw_data)

    # Lots of data, yes, but it is necessary to stramline the upcoming processes
    return raw_data, was_redirected, search_url, final_url, website_name, http_code, success_flag, url_list, text_list


pass