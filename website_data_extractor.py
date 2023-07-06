# This script extracts and saves all useful data from a single website
import os
import urllib.request
import parser_l



def sanitize_url_to_name(input):
   removal_list = ['http://', 'https://', 'www.']
   
   output = input
   for item in removal_list:
      output = output.replace(item, '')
   
   if output[-1] == '/':
      output = output[:-1]

   return output

def extract_html(url):
   url = sanitize_url_to_name(url)
   url = 'http://' + url
   try:
      with urllib.request.urlopen(url) as response:
         html = response.read()
      return html
   except:
      return ''


def get_website_data(url):
    website_name = sanitize_url_to_name(url)

    raw_file_data = extract_html(url)
    html_data = parser_l.byte_to_string(raw_file_data)

    link_list = parser_l.link_parser(html_data)
    text_list = parser_l.text_parser(html_data)

    return website_name, raw_file_data, link_list, text_list

pass