# This script saves important data from the website and returns paths for the data.
import os
import time
from . import website_data_extractor as site_ex

def main_folders_manager():
    global ALL_WEBSITES_FOLDER
    #database_dir = os.path.dirname(os.path.dirname(__file__))
    database_dir = ''
    ALL_WEBSITES_FOLDER = os.path.join(database_dir, ALL_WEBSITES_FOLDER)
    if(not os.path.exists(ALL_WEBSITES_FOLDER)):
        os.mkdir(ALL_WEBSITES_FOLDER)

def get_pages_database_path():
    # The indexer will need to know where the pages are located
    return ALL_WEBSITES_FOLDER

def get_filenames():
    global DATA_FILENAME
    global LINK_LIST_FILENAME
    global TEXT_LIST_FILENAME
    global META_LIST_FILENAME

    return (DATA_FILENAME, LINK_LIST_FILENAME,
            TEXT_LIST_FILENAME, META_LIST_FILENAME)


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

def load_list_from_file(in_file):
    try:
        with open(in_file, 'rb') as file:
            data = (file.read()).decode('utf-8')
            if data == '':
                #raise EmptyListException
                return ''
            list = data.split('\n')
            return list
    except FileNotFoundError:
        return FileNotFoundError

def website_path(name):
    global DATA_FILENAME
    global LINK_LIST_FILENAME
    global TEXT_LIST_FILENAME
    global META_LIST_FILENAME

    aux = name
    data_file, link_list_file, text_list_file, meta_list_file = '', '', '', ''
    if '/' in aux:
        aux = aux.split('/')
    else:
        aux = [aux]
    aux.insert(0, ALL_WEBSITES_FOLDER)
    website_folder = aux[0]

    error = False
    level_counter = 0
    for level in range(len(aux)-1):
        website_folder = os.path.join(website_folder, aux[level+1])
        level_counter += 1

        if(not os.path.exists(website_folder)):
            try:
                os.mkdir(website_folder)
            except FileNotFoundError:
                print('FileNotFoundError EXCEPTION!')
                error = True
                break
    
    #Undo the file creation if it failed
    if error:
        for i in range(level_counter-1):
            website_folder = os.path.split(website_folder)[0]
            try:
                os.rmdir(website_folder)
            except OSError:
                break
        return data_file, link_list_file, text_list_file, meta_list_file
        

    data_file = os.path.join(website_folder, DATA_FILENAME)
    link_list_file = os.path.join(website_folder, LINK_LIST_FILENAME)
    text_list_file = os.path.join(website_folder, TEXT_LIST_FILENAME)
    meta_list_file = os.path.join(website_folder, META_LIST_FILENAME)

    return data_file, link_list_file, text_list_file, meta_list_file

def get_website(search_url): # Rename later to 'save_website'
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
    is_page = len(link_list) != 0 and len(text_list) != 0
    # But if you reeeeeealy want to index images and files as well,
    # I'm giving you the option to.
    # Be aware: Not having text or links does not mean it is surely an image
    i_really_want_to_index_images_and_whatnot = False

    
    if is_page or i_really_want_to_index_images_and_whatnot:
        # Get paths
        data_file, link_list_file, text_list_file, meta_list_file = website_path(website_name)
    
    
    if len(raw_file_data) == 0: # If it has no data, there is nothing to index
        return data_file, link_list_file, text_list_file, meta_list_file
    
    # Save data in folder
    if not is_page: # If the link is a page, do not save raw data
        save_html_to_file(raw_file_data, data_file) # Save raw html/data
    if len(link_list) != 0:
        save_list_to_file(link_list, link_list_file) # Save links
    if len(text_list) != 0:
        save_list_to_file(text_list, text_list_file) # Save text
    
    
    save_list_to_file(meta_list, meta_list_file)

    return data_file, link_list_file, text_list_file, meta_list_file


DATA_FILENAME = 'data.txt'
LINK_LIST_FILENAME = 'links.txt'
TEXT_LIST_FILENAME = 'text.txt'
META_LIST_FILENAME = 'meta.txt'


ALL_WEBSITES_FOLDER = 'SITES_INDEX'
main_folders_manager()
