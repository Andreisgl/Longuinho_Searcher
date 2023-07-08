# This script parses downloaded webpages for links and text

import os
import re
from bs4 import BeautifulSoup


def find_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

def remove_whitespaces_from_list(in_list):
    for index in range(len(in_list)):
        in_list[index] = in_list[index].strip()
    in_list = [x for x in in_list if x != '']

    return in_list

def cleanhtml(raw_html):
  CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext


def get_file_data(filepath):
    # Get raw html data from file
    filedata = ''
    with open(filepath, 'rb') as file:
        filedata = file.read()
        filedata = byte_to_string(filedata)
    return filedata

def byte_to_string(filedata):
    try:
        return filedata.decode('utf-8')
    except:
        return ''

def link_parser(file_data):
    # Returns all links found in the page
    link_parse_data = file_data.split('\n')
    link_parse_data = remove_whitespaces_from_list(link_parse_data)
    
    temp_list = []
    for index in link_parse_data:
        
        # IGNORE DANGEROUS ENTRIES!!!
        if '\'' in index or '\"\"' in index or '\\' in index:
            continue

        search = find_url(index)

        if len(search) >= 1:
            for item in search:
                temp_list.append(item)
    return temp_list

def text_parser(file_data):
    # Return all blocks of text in the file
    soup = BeautifulSoup(file_data, "html.parser")

    # Split on newlines
    text = soup.get_text()
    text = text.split('\n')
    #Remove '\t's
    for index in range(len(text)):
        text[index] = text[index].replace('\t', '')
    #Remove empty elements from list
    try:
        while True:
            text.remove('')
    except ValueError:
        pass    
    return text








#link_list = link_parser(get_file_data(test_file))
#text_list = text_parser(get_file_data(test_file))



pass