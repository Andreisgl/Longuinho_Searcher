# This script extracts and saves all useful data from a single website
import os
import urllib.request
from . import parser_l

illegal_filename_characters = ['#', '<', '$', '+', '%','>', '!', '`', '&', '*', "'", '|', '{', '?', '"', '=', '}', ':', '\\', '\xa0', '@', ';']
# removed '/', since it is needed for diferent levels
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
   #TODO: add headers to pass as browser
   url = sanitize_url_to_name(url)
   url = 'http://' + url
   




   try:
      with urllib.request.urlopen(url, timeout = 20.0) as response:
         html = response.read()
      return html
   except TimeoutError:
      print('TIMEOUT @ ' + url)
   except urllib.error.HTTPError as e:
      if e.status != 307:
         raise  # not a status code that can be handled here
      redirected_url = urllib.parse.urljoin(url, e.headers['Location'])
      resp = urllib.request.urlopen(redirected_url)
      print('Redirected -> %s' % redirected_url)  # the original redirected url 
   print('Response URL -> %s ' % resp.url)  # the final url
   #except:
   #   print('UNKNOWN HTML ERROR')
   return b''


def get_website_data(url):
    website_name = sanitize_url_to_filesystem(url)

    raw_file_data = extract_html(url)
    html_data = parser_l.byte_to_string(raw_file_data)

    link_list = parser_l.link_parser(html_data)
    text_list = parser_l.text_parser(html_data)

    return website_name, raw_file_data, link_list, text_list

pass