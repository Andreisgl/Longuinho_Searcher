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
   while True:
      real_url = url
      error_code = ''
      url = sanitize_url_to_name(url)
      url = 'http://' + url


      # pass_over_retry
      # If 'True', skip URL
      # If 'False', retry
      # Retry only if connection problem is suspected.
      # Other errors shall return empty data
      pass_over_retry = None


      try:
         with urllib.request.urlopen(url, timeout = 20.0) as response:
            html = response.read()
         real_url = response.url
         http_code = response.status
         return html, real_url

      except urllib.error.URLError as e: # Unable to access URL
         if e.reason.errno == 11001:
            error_code = e.reason.errno
         else:
            error_code = e.code
         
      except:
         error_code = '?'

      print('ERROR CODE: {}'.format(error_code))

      if error_code == 11001: # Connection problem
         print('CHECK YOUR CONNECTION!!')
         input('Press enter to retry\n') # Freeze code
         continue # Retry

      elif error_code == 403: # Forbidden
         pass # Do not attempt to retry
      else:
         pass
      break # Proceed to return empty values

   return b'', real_url # Return empty data


def get_website_data(url):
   raw_file_data, real_url = extract_html(url)
   html_data = parser_l.byte_to_string(raw_file_data)

   link_list = parser_l.link_parser(html_data)
   text_list = parser_l.text_parser(html_data)

   website_name = sanitize_url_to_filesystem(real_url)

   return website_name, raw_file_data, link_list, text_list, real_url

pass