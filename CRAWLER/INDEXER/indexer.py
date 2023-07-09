# This script saves important data from the website and returns paths for the data.
import os
import time
from . import website_data_extractor as site_ex

ALL_WEBSITES_FOLDER = 'SITES'

def main_folders_manager():
    global ALL_WEBSITES_FOLDER
    basedir = os.path.dirname(os.path.dirname(__file__))
    ALL_WEBSITES_FOLDER = os.path.join(basedir, ALL_WEBSITES_FOLDER)
    if(not os.path.exists(ALL_WEBSITES_FOLDER)):
        os.mkdir(ALL_WEBSITES_FOLDER)

def save_html_to_file(html, filepath):
   try:
       with open(filepath, 'wb') as file:
           file.write(html)
   except FileNotFoundError:
       pass

def save_list_to_file(list, path):
    try:
        with open(path, 'wb') as file:
            for index in range(len(list)):
                aux = list[index].encode('utf-8')
                file.write(aux)
                if index != len(list)-1:
                    file.write(b'\n')
    except FileNotFoundError:
       pass

def website_path(name):
    aux = name
    data_file, link_list_file, text_list_file, meta_list_file = '', '', '', ''
    if '/' in aux:
        aux = aux.split('/')
    else:
        aux = [aux]
    aux.insert(0, ALL_WEBSITES_FOLDER)
    website_folder = aux[0]
    for level in range(len(aux)-1):
        website_folder = os.path.join(website_folder, aux[level+1])
        if(not os.path.exists(website_folder)):
            try:
                os.mkdir(website_folder)
            except FileNotFoundError:
                print('FileNotFoundError EXCEPTION!')
                return data_file, link_list_file, text_list_file, meta_list_file

    data_file = 'data.txt'
    data_file = os.path.join(website_folder, data_file)

    link_list_file = 'links.txt'
    link_list_file = os.path.join(website_folder, link_list_file)

    text_list_file = 'text.txt'
    text_list_file = os.path.join(website_folder, text_list_file)

    meta_list_file = 'meta.txt'
    meta_list_file = os.path.join(website_folder, meta_list_file)

    return data_file, link_list_file, text_list_file, meta_list_file

def get_website(search_url):
    # Saves important data from the website, returns paths for the data.
    data_file = ''
    link_list_file = ''
    text_list_file = ''
    meta_list_file = ''

    (website_name,
     raw_file_data,
     link_list,
     text_list) = site_ex.get_website_data(search_url)

    # CREATE METADATA
    meta_url = 'URL\{}'.format(search_url)
    now = time.time()
    meta_datetime_local=time.strftime('%Y-%m-%d %H:%M %Z',time.localtime(now))
    meta_datetime_gmt = time.strftime('%Y-%m-%d %H:%M %Z', time.gmtime(now))
    
    meta_datetime_local = 'DATEINDEXEDLOCAL\{}'.format(meta_datetime_local)
    meta_datetime_gmt = 'DATEINDEXEDGMT\{}'.format(meta_datetime_gmt[:16])
    meta_list = [meta_url,
                 meta_datetime_local,
                 meta_datetime_gmt]
    ###

    # If it has no links and no text, it is probably an image or file.
    # Not worthy of indexing and just occupies space.
    indexing_condition = len(link_list) != 0 and len(text_list) != 0
    # But if you reeeeeealy want to index images and files as well,
    # I'm giving you the option to.
    # Be aware: Not having text or links does not mean it is surely an image
    i_really_want_to_index_images_and_whatnot = False

    
    if indexing_condition or i_really_want_to_index_images_and_whatnot:
        # Get paths
        data_file, link_list_file, text_list_file, meta_list_file = website_path(website_name)
    
    
    # Save data in folder
    if len(raw_file_data) == 0: # If it has no data, there is nothing to index
        return data_file, link_list_file, text_list_file, meta_list_file
    
    save_html_to_file(raw_file_data, data_file) # Save raw html/data
    if len(link_list) != 0:
        save_list_to_file(link_list, link_list_file) # Save links
    if len(text_list) != 0:
        save_list_to_file(text_list, text_list_file) # Save text
    
    
    save_list_to_file(meta_list, meta_list_file)

    return data_file, link_list_file, text_list_file, meta_list_file

main_folders_manager()
