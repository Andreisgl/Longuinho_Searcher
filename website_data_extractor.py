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
   with urllib.request.urlopen(url) as response:
      html = response.read()
   return html

def website_path_creator(search_url):
    #website_folder
    #website_name
    website_name = sanitize_url_to_name(search_url)
    website_folder = ''
    website_folder = os.path.join(ALL_WEBSITES_FOLDER, website_name)
    #if(not os.path.exists(website_folder)):
    #    os.mkdir(website_folder)


    #data_file
    data_file = "data.txt"
    data_file = os.path.join(website_folder, data_file)


    #link_list_file
    link_list_file = 'links.txt'
    link_list_file = os.path.join(website_folder, link_list_file)

    #text_list_file
    text_list_file = 'text.txt'
    text_list_file = os.path.join(website_folder, text_list_file)

    return website_name, data_file, link_list_file, text_list_file





def get_website_data(url):

    website_name, data_file, link_list_file, text_list_file = website_path_creator(url)

    raw_file_data = extract_html(url)
    html_data = parser_l.byte_to_string(raw_file_data)

    link_list = parser_l.link_parser(html_data)
    text_list = parser_l.text_parser(html_data)

    # Save data in folder
    #save_html_to_file(raw_file_data, data_file) # Save raw html
    #save_list_to_file(link_list, link_list_file) # Save links
    #save_list_to_file(text_list, text_list_file) # Save text

    #return data_file, link_list_file, text_list_file
    return website_name, raw_file_data, link_list, text_list


ALL_WEBSITES_FOLDER = 'SITES'



#main_folders_manager()

#get_website_data(search_url)

pass