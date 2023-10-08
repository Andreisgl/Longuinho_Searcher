# This script saves important data from the website and returns paths for the data.
import os
import shutil
import time

import textwrap

import website_extractor as site_ex

def main_folders_manager():
    global ALL_WEBSITES_FOLDER
    #database_dir = os.path.dirname(os.path.dirname(__file__))
    database_dir = ''
    ALL_WEBSITES_FOLDER = os.path.join(database_dir, ALL_WEBSITES_FOLDER)
    if(not os.path.exists(ALL_WEBSITES_FOLDER)):
        os.mkdir(ALL_WEBSITES_FOLDER)

# DISPLAY STUFF
def get_terminal_columns():
    return shutil.get_terminal_size().columns
no_terminal_columns = get_terminal_columns()


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
        with open(in_file, 'w'):
            pass
        return ''

def save_new_meta_file(meta_list, link_list, text_list, raw_data, path):
        # Put all data in meta file
        # Offsets indicate where each sector starts

        all_data = []
        all_data.append(meta_list)
        all_data.append(link_list)
        all_data.append(text_list)

        #all_data.append(raw_data) # Don't save raw html data. TODO: Add option to toogle the saving of raw html


        # Assemble data to file
        final_data = b''
        with open(path, 'w+b') as file:
            offset_list = []
            for sector in all_data:
                #offset_list.append(file.tell())
                offset_list.append(len(final_data))
                if type(sector) == list:
                    for index, line in enumerate(sector):
                        aux = line.encode('utf-8')
                        #file.write(aux)
                        final_data += aux
                        if index != len(sector)-1:
                            #file.write(b'\n')
                            final_data += b'\n'
                else:
                    #file.write(sector)
                    final_data += sector
                final_data += b'\n'
        
            # CREATE HEADER
            # In how many bytes each offset in the header will be represented with
            bytes_per_offset = 8
            number_of_offsets = len(offset_list)
            # +1 to include number of sectors in the first entry
            number_of_entries_in_header = number_of_offsets + 1
            extra_bytes_in_offsets = number_of_entries_in_header * bytes_per_offset

            # Add extra bytes to all offsets
            offset_list = [x + extra_bytes_in_offsets for x in offset_list]

            # Write header
            #file.seek(0, 0)
            #read_data = file.read()
            #file.seek(0, 0)

            write_data = int.to_bytes(number_of_offsets, bytes_per_offset, 'little')
            file.write(write_data)
            for offset in offset_list:
                write_data = int.to_bytes(offset, bytes_per_offset, 'little')
                file.write(write_data)

            # Write previous data
            #file.write(read_data)
            file.write(final_data)

def website_path(name):
    global META_LIST_FILENAME
    file_extension = 'longsp'

    aux = name
    meta_list_file = ''
    if '/' in aux:
        aux = aux.split('/')
    else:
        aux = [aux]
    aux.insert(0, ALL_WEBSITES_FOLDER)
    all_websites_folder = aux[0]
    website_folder = aux[1]
    page_path = os.path.join(all_websites_folder, website_folder)
    
    if not os.path.exists(page_path):
        os.mkdir(page_path)
    

    def autoincrement_filename(dir_path, extension):
        ''' Implements autoincrement.
        Returns the next number the filename can have'''
        name_list = os.listdir(dir_path)
        name_list = [int(x.split('.')[0]) for x in name_list]
        smallest_missing = 1

        while smallest_missing in name_list:
            smallest_missing += 1
        
        return '{}.{}'.format(smallest_missing, extension)

    def url_filename(dir_path, extension):
        file_name = ''
        separator_char = '.'
        if len(aux) >= 3:
            workset = aux[2:]
            interval = enumerate(workset)
            for index, level in interval:
                file_name += level
                if index != len(workset)-1:
                    file_name += separator_char
        else:
            file_name = aux[1]

        file_name = '{}.{}'.format(file_name, file_extension)
        return file_name
    
    #final_filename = url_filename(page_path, file_extension)
    final_filename = meta_list_file = autoincrement_filename(page_path, file_extension)

    meta_list_file = os.path.join(page_path, final_filename)

    return meta_list_file

def save_website(search_url): # Rename later to 'save_website'
    # Saves important data from the website, returns paths for the data.
    meta_list_file = ''

    #(website_name, raw_file_data, link_list, text_list, real_url) = site_ex.get_data_from_url(search_url)
    (raw_file_data,
     was_redirected, search_url, real_url, website_name,
     http_code, success_flag,
     link_list, text_list) = site_ex.get_data_from_url(search_url)

    # Prints
    # Print current URL
    display_url = textwrap.wrap(search_url, no_terminal_columns-1)
    print('{}'.format(display_url[0]))

    # Save to history
    if was_redirected:
        # Print final URL
        print('REDIRECTED TO:')
        display_url = textwrap.wrap(real_url, no_terminal_columns-1)
        print('{}'.format(display_url[0]))


    # CREATE METADATA
    meta_url = 'URL\{}'.format(real_url)
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
    index_condition = is_page or i_really_want_to_index_images_and_whatnot


    return_data = (was_redirected, search_url, real_url,
                   link_list, text_list)
    

    if not index_condition:
        return return_data # Return without saving page
    

    # Get paths for saving
    meta_list_file = website_path(website_name)
    # Save page
    save_new_meta_file(meta_list, link_list, text_list, raw_file_data, meta_list_file)

    return return_data



META_LIST_FILENAME = 'meta.txt'


ALL_WEBSITES_FOLDER = 'SITES_INDEX'
main_folders_manager()

pass