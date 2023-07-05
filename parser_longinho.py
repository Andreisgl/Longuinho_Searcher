# This script parses downloaded webpages for links and text

import os
import re






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


test_folder = 'TESTE'
test_file = "teste.txt"

test_folder = os.path.join('.\\', test_folder)
test_file = os.path.join(test_folder, test_file)


# Get data from file
filedata = ''
with open(test_file, 'r') as file:
    filedata = file.read()


def link_parser(input):
    # Returns all links found in the page
    link_parse_data = input.split('\n')
    link_parse_data = remove_whitespaces_from_list(link_parse_data)

    temp_list = []
    for index in link_parse_data:
        search = find_url(index)
        if len(search) >= 1:
            for item in search:
                temp_list.append(item)
    return temp_list

link_list = link_parser(filedata)





def text_parser(input):
    # Parse for text
    text_parse_data = input
    text_parse_data = cleanhtml(text_parse_data)
    text_parse_data = text_parse_data.split('\n')
    text_parse_data = remove_whitespaces_from_list(text_parse_data)
    return text_parse_data



text_list = text_parser(filedata)










pass