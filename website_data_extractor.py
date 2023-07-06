# This script extracts and saves all useful data from a single website
import os
import urllib.request
import parser_l

illegal_filename_characters = ['#', '<', '$', '+', '%','>', '!', '`', '&', '*', "'", '|', '{', '?', '"', '=', '}', ':', '\\', '\xa0', '@', ';']
# remove '/', since it is needed for diferent levels
translation_characters = ['☺', '☻', '♥', '♦', '♣', '♠', '•', '○', '◙', '♂', '♀', '♪', '♫', '☼', '►', '◄', '↕', '‼', '¶', '§', '▬', '↨']


def sanitize_url_to_name(input):
   removal_list = ['http://', 'https://', 'www.']
   
   output = input
   for item in removal_list:
      output = output.replace(item, '')
   
   if output[-1] == '/':
      output = output[:-1]

   return output

def sanitize_url_to_filesystem(input):
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

def extract_html(url):
   url = sanitize_url_to_name(url)
   url = 'http://' + url
   try:
      with urllib.request.urlopen(url) as response:
         html = response.read()
      return html
   except:
      print('HTML error @ ' + url)
      return b''


def get_website_data(url):
    website_name = sanitize_url_to_filesystem(url)

    raw_file_data = extract_html(url)
    html_data = parser_l.byte_to_string(raw_file_data)

    link_list = parser_l.link_parser(html_data)
    text_list = parser_l.text_parser(html_data)

    return website_name, raw_file_data, link_list, text_list

pass