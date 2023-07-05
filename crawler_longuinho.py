# This file centralizes the full functionality of the crawler.
import os

import url_extractor
import parser_longuinho

def sanitize_url_to_name(input):
   removal_list = ['http://', 'https://', 'www.']
   
   output = input
   for item in removal_list:
      output = output.replace(item, '')
   
   if output[-1] == '/':
      output = output[:-1]

   return output

def main_folders_manager():
    global ALL_WEBSITES_FOLDER
    ALL_WEBSITES_FOLDER = os.path.join('.\\', ALL_WEBSITES_FOLDER)
    if(not os.path.exists(ALL_WEBSITES_FOLDER)):
        os.mkdir(ALL_WEBSITES_FOLDER)

def website_path_creator(search_url):
    global website_folder
    global website_name
    global data_file

    website_name = sanitize_url_to_name(search_url)

    website_folder = ''
    website_folder = os.path.join(ALL_WEBSITES_FOLDER, website_name)

    data_file = "data.txt"
    data_file = os.path.join(website_folder, data_file)

    if(not os.path.exists(website_folder)):
        os.mkdir(website_folder)

def save_html_to_file(html, filepath):
   with open(filepath, 'wb') as file:
      file.write(html)


ALL_WEBSITES_FOLDER = 'SITES'
main_folders_manager()



search_url = 'http://hashomer.org.br/'



website_folder = ''
website_name = ''
data_file = ''
file_data = ''

website_path_creator(search_url)

file_data = url_extractor.extract_html(search_url)
html_data = parser_longuinho.byte_to_string(file_data)

link_list = parser_longuinho.link_parser(html_data)
text_list = parser_longuinho.text_parser(html_data)


# Save data in folder
save_html_to_file(file_data, data_file)
# Implement save text blocks later

link_list_file = 'links.txt'
link_list_file = os.path.join(website_folder, link_list_file)
with open(link_list_file, 'w') as file:
   for item in link_list:
      file.write(item)
      file.write('\n')
   pass


pass