# This script parses downloaded webpages for links and text

import os
import re
from bs4 import BeautifulSoup


def find_url(string):
    pass
    urlsoup = BeautifulSoup(string, 'html.parser')
    aux = urlsoup.find_all('a')
    return [x.get('href') for x in aux
            if x.get('href') != None and x.get('href').startswith('http')]

def remove_whitespaces_from_list(in_list): # Unused function? Check better later
    for index in range(len(in_list)):
        in_list[index] = in_list[index].strip()
    in_list = [x for x in in_list if x != '']

    return in_list

def cleanhtml(raw_html): #TODO FUNCTION UNUSED!!!
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
    receive = find_url(file_data)
    output = []
    for url in receive:
        # IGNORE DANGEROUS ENTRIES!!!
        if not ('\'' in url or '\"\"' in url or '\\' in url):
            output.append(url)
    return output

def text_parser(file_data):
    # Return all blocks of text in the file
    textsoup = BeautifulSoup(file_data, "html.parser")

    # Split on newlines
    text = textsoup.get_text()
    text = text.split('\n')
    #Remove '\t's
    for index in range(len(text)):
        text[index] = text[index].replace('\t', '')
    
    #Remove empty elements from list
    return [line for line in text if line != '']