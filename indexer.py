# This script sets up the links obtained in a indexed website to crawl.
import os
import website_data_extractor as site_ex

ALL_WEBSITES_FOLDER = 'SITES'
def main_folders_manager():
    global ALL_WEBSITES_FOLDER
    ALL_WEBSITES_FOLDER = os.path.join('.\\', ALL_WEBSITES_FOLDER)
    if(not os.path.exists(ALL_WEBSITES_FOLDER)):
        os.mkdir(ALL_WEBSITES_FOLDER)

def save_html_to_file(html, filepath):
   with open(filepath, 'wb') as file:
      file.write(html)

def save_list_to_file(list, path):
   with open(path, 'wb') as file:
    for item in list:
        aux = item.encode('utf-8')
        file.write(aux)
        file.write(b'\n')

def create_website_folder(website_name):
    website_folder = ''
    website_folder = os.path.join(ALL_WEBSITES_FOLDER, website_name)
    if(not os.path.exists(website_folder)):
        os.mkdir(website_folder)
    return website_folder


search_url = 'http://hashomer.org.br/'
website_name, raw_file_data, link_list, text_list = site_ex.get_website_data(search_url)

main_folders_manager()

website_folder = create_website_folder(website_name)
data_file = 'data.txt'
data_file = os.path.join(website_folder, data_file)

link_list_file = 'links.txt'
link_list_file = os.path.join(website_folder, link_list_file)

text_list_file = 'text.txt'
text_list_file = os.path.join(website_folder, text_list_file)


# Save data in folder
save_html_to_file(raw_file_data, data_file) # Save raw html
save_list_to_file(link_list, link_list_file) # Save links
save_list_to_file(text_list, text_list_file) # Save text

pass