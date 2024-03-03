# This script crawls a list of URLs, gets all links present in them
# and appends those to the list

import os
import shutil
import time

import textwrap
from multiprocessing import Pool
import csv

from website_extractor import get_data_from_url
from site_saver import save_website


# DISPLAY STUFF
def get_terminal_columns():
    return shutil.get_terminal_size().columns
no_terminal_columns = get_terminal_columns()


# MAIN PATHS MANAGER
def main_paths_manager():
    # This function creates and completes the paths
    # for important files and folders
    
    def check_file(path):
        # Creates file it it does not exis already
        if not os.path.exists(path): # Create file if it does not exist
            with open(path, 'w'):
                pass

    def check_folder(path):
        # Creates folder it it does not exis already
        if not os.path.exists(path):
            os.mkdir(path)

    # Main folder
    global MAIN_FOLDER
    check_folder(MAIN_FOLDER)

    # incoming_url_list_file
    global incoming_url_list_file
    incoming_url_list_file = os.path.join(MAIN_FOLDER, incoming_url_list_file)
    check_file(incoming_url_list_file)

    # url_history_list_file
    global url_history_list_file
    url_history_list_file = os.path.join(MAIN_FOLDER, url_history_list_file)
    check_file(url_history_list_file)
    
    #seed_list_file
    global seed_list_file
    seed_list_file = os.path.join(MAIN_FOLDER, seed_list_file)
    check_file(seed_list_file)
    
    #blacklist_list_file
    global blacklist_list_file
    blacklist_list_file = os.path.join(MAIN_FOLDER, blacklist_list_file)
    #if not os.path.exists(blacklist_list_file): # Create file if it does not exist
    #    with open(blacklist_list_file, 'w'):
    #        pass
    check_file(blacklist_list_file)

# LIST SAVING MANAGEMENT
def save_list_in_file(in_list, filepath):
    # Saves a list as lines in a file
    # Returns 'True' if succeeded,
    # 'False' if failed.

    try:
        with open(filepath, 'wb') as file:
            for index, item in enumerate(in_list):
                file.write(item.encode('utf-8'))
                if index < len(in_list)-1:
                    file.write('\n'.encode('utf-8'))
        return True
    except:
        return False
def load_list_from_file(file_path):
    # Returns a list containing all lines in a file

    data = ''
    with open(file_path, 'rb') as file:
        data = (file.read()).decode('utf-8')
    if data != '':
        data = data.split('\n')
    
    return data

# INCOMING LIST MANAGEMENT
def save_incoming_to_file():
    # Saves 'incoming_url_list' to its respective file
    global incoming_url_list
    global incoming_url_list_file
    save_list_in_file(incoming_url_list, incoming_url_list_file)
def load_incoming_from_file():
    # Saves 'incoming_url_list' from its respective file
    global incoming_url_list
    global incoming_url_list_file
    incoming_url_list = load_list_from_file(incoming_url_list_file)
    if incoming_url_list == '':
        incoming_url_list = []

# HISTORY LIST MANAGEMENT
def save_history_to_file():
    # Saves 'history_list' to its respective file
    global url_history_list
    global url_history_list_file
    save_list_in_file(url_history_list, url_history_list_file)
def load_history_from_file():
    # Saves 'history_list' from its respective file
    global url_history_list
    global url_history_list_file
    url_history_list = load_list_from_file(url_history_list_file)
    if url_history_list == '':
        url_history_list = []

# BLACKLIST LIST MANAGEMENT
def load_blacklist_from_file():
    # Saves 'history_list' from its respective file
    global blacklist_list
    global blacklist_list_file
    blacklist_list = load_list_from_file(blacklist_list_file)
    if blacklist_list == '':
        blacklist_list = []

# MORE LIST STUFF
def translate_list_of_list(in_list, encode_flag):
    # This functions translate lists of lists to a file-saveable format
    # encode_flag:
    #   if 'True', it encodes from normal list to saveable list
    #   if 'False', it encodes from saveable list to normal list
    # END FORMAT:
    #   normal_list = [['a', 'b', 'c'], [['apple', 'banana'], '2', '3']]
    #   saveable_list = ['a|b|c','apple^banana|2|3']
    #   This method suports up to a triple-nested list
    #   A list inside a list inside a list: [ [ [] ] ]
    # This is messy, I know. That's how I was able to do it.
    
    separation_char1 = '|*|'
    separation_char2 = '^*^'
    out_list = []
    intermediate_list = []
    if encode_flag: # Normal to saveable
        for pack in in_list:
            pack_substring = ''
            for index, item in enumerate(pack):
                if type(item) == str:
                    pack_substring += item
                if type(item) == bytes:
                    item = item.decode('utf-8')
                if type(item) == bool:
                    # Convert bool values to string
                    if item:
                        item = 'True'
                    else:
                        item = 'False'
                if type(item) == int:
                    item = str(item)
                if type(item) == list:
                    sub_substring = ''
                    for index2, subitem in enumerate(item):
                        if type(subitem) == str:
                            sub_substring += subitem
                        if index2 < len(item)-1:
                            sub_substring += separation_char2
                    item = sub_substring

                pack_substring += item

                if index < len(pack)-1:
                    pack_substring += separation_char1
                pass
            out_list.append(pack_substring)
    else: # Saveable to normal:
        for pack in in_list:
            # Divide into normal structure
            pack = pack.split(separation_char1)
            # Unpack link and text lists
            pack[5] = pack[5].split(separation_char2)
            pack[6] = pack[6].split(separation_char2)
            out_list.append(pack)

        pass
    return out_list


# LIST CLEANING
def remove_duplicates_from_list(input_list):
    '''Returns the list without duplicates
    and ammount of entries removed.'''

    process_list = input_list # Assign to avoid reference passes
    initial_length = len(process_list)
    # Transforming to 'dictionary removes duplicates
    process_list = list(dict.fromkeys(process_list))
    final_length = len(process_list)

    return process_list, (initial_length - final_length)
def remove_entries_from_another_list(target_list, tool_list):
    '''Returns the 'target_list' without 'tool_list' entries
    and ammount of entries removed.'''

    initial_length = len(target_list)

    target_set = set(target_list)
    tool_set = set(tool_list)

    final_set = target_set.difference(tool_set)
    final_list = list(final_set)
    
    final_length = len(final_list)

    return final_list, (initial_length - final_length)

# MAIN LIST MANAGEMENT AND CLEANING
def remove_duplicates_from_incoming():
    # Removes duplicates from 'incoming',
    # returns ammount of URLs removed.
    # Only use when 'incoming_link_queue' is already loaded
    global incoming_url_list

    (incoming_url_list,
     amt_removed
     ) = remove_duplicates_from_list(incoming_url_list)
    
    return amt_removed
def removed_links_in_history_from_incoming():
    # Removes from 'incoming' URLs already present in 'history',
    # returns ammount of URLs removed
    # Only use when both lists are already loaded
    global incoming_url_list
    global url_history_list

    (incoming_url_list,
     amt_removed
     ) = remove_entries_from_another_list(incoming_url_list, url_history_list)

    return amt_removed
def remove_blacklisted_sites_from_incoming():
    # Some sites just take too long to load, like the web.archive.
    # This allows to remove them from the incoming list.
    # Returns number of excluded terms.
    # Only use when 'incoming_link_queue' is already loaded

    global incoming_url_list
    global blacklist_list
    
    load_blacklist_from_file()
    
    # Add prefixes to each website so they reflect their counterparts
    # in 'incoming'
    prefixes = ['', 'http://', 'https://']
    full_terms = []

    initial_length = len(incoming_url_list)

    for site in blacklist_list:
        for prefix in prefixes:
            full_terms.append(prefix + site)
    
    for index, url in enumerate(incoming_url_list):
        for site in full_terms:
            if url.startswith(site):
                incoming_url_list.pop(index)
    
    final_length = len(incoming_url_list)

    return initial_length - final_length
def clean_incoming():
    # Unifies all cleaning methos into a single call
    # Returns total ammount of URLs removed
    # Only use when 'incoming_link_queue' is already loaded

    removed_counter = 0
    duplicate_start_time = time.perf_counter()
    duplicate_counter = remove_duplicates_from_incoming()
    duplicate_finish_time = time.perf_counter()
    
    existing_start_time = time.perf_counter()
    existing_counter = removed_links_in_history_from_incoming()
    existing_finish_time = time.perf_counter()

    blacklist_start_time = time.perf_counter()
    blacklisted_counter = remove_blacklisted_sites_from_incoming()
    blacklist_finish_time = time.perf_counter()

    removed_counter = (duplicate_counter
                       + existing_counter
                       + blacklisted_counter)
    
    print('\nRemoved {} pages:\n{} duplicates,\n{} existing\n{} blacklisted'
          .format(removed_counter, duplicate_counter,
                  existing_counter, blacklisted_counter))
    
    show_debugging_timings = False
    if show_debugging_timings:
        duplicate_time = duplicate_finish_time - duplicate_start_time
        existing_time = existing_finish_time - existing_start_time
        blacklist_time = blacklist_finish_time - blacklist_start_time

        print('Incoming Cleaning: Time per section:')
        print('Duplicates: {} seconds'.format(duplicate_time))
        print('Existing: {} seconds'.format(existing_time))
        print('Blacklist: {} seconds'.format(blacklist_time))
    return removed_counter


# STATISTICS:
def count_pages_crawled():
    global url_history_list
    global redirector_flag
    load_history_from_file()
    real_indexed_list = [x for x in url_history_list if redirector_flag not in x]
    return len(real_indexed_list)

# CRAWLING
def plant_seed():
    global incoming_url_list
    global seed_list
    global seed_list_file

    seed_list = load_list_from_file(seed_list_file)
    
    for seed in seed_list:
        incoming_url_list.append(seed)
    save_incoming_to_file()

def pathfinder():
    '''Crawls a list and'''
    


# MAIN

def main():
    print('This is the Longin Crawler!')
    load_history_from_file()
    print('Ammount of pages already crawled: {}'.format(count_pages_crawled()))
    while True:
        try:
            answer = int(input('How many pages do you want to index? '))
        except ValueError:
            print('Input a valid number!')
            continue
        expand_index(answer)
        break

    print('Ammount of pages already crawled: {}'.format(count_pages_crawled()))
    input('Done! Press ENTER to exit')

MAIN_FOLDER = 'crawler_data'

incoming_url_list = []
incoming_url_list_file = 'queue.txt'

url_history_list = []
url_history_list_file = 'history.txt'

seed_list = []
seed_list_file = 'seeds.txt'

blacklist_list = []
blacklist_list_file = 'blacklist.txt'

# If the called link redirected to somewhere else,
# Mark it so it is included in history,
# but not counted as an indexed page
redirector_flag = '´'


main_paths_manager()

if __name__ == '__main__':
    main()




pass