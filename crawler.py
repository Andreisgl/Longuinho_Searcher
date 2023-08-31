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

def main_paths_manager():
    # This function creates and completes the paths
    # for important files and folders
    
    # Main folder
    global MAIN_FOLDER
    if not os.path.exists(MAIN_FOLDER):
        os.mkdir(MAIN_FOLDER)

    # incoming_url_list_file
    global incoming_url_list_file
    incoming_url_list_file = os.path.join(MAIN_FOLDER, incoming_url_list_file)
    if not os.path.exists(incoming_url_list_file): # Create file if it does not exist
        with open(incoming_url_list_file, 'w'):
            pass

    # url_history_list_file
    global url_history_list_file
    url_history_list_file = os.path.join(MAIN_FOLDER, url_history_list_file)
    if not os.path.exists(url_history_list_file): # Create file if it does not exist
        with open(url_history_list_file, 'w'):
            pass
    
    #seed_list_file
    global seed_list_file
    seed_list_file = os.path.join(MAIN_FOLDER, seed_list_file)
    if not os.path.exists(seed_list_file): # Create file if it does not exist
        with open(seed_list_file, 'w'):
            pass
    
    #blacklist_list_file
    global blacklist_list_file
    blacklist_list_file = os.path.join(MAIN_FOLDER, blacklist_list_file)
    if not os.path.exists(blacklist_list_file): # Create file if it does not exist
        with open(blacklist_list_file, 'w'):
            pass

# DISPLAY STUFF
def get_terminal_columns():
    return shutil.get_terminal_size().columns
no_terminal_columns = get_terminal_columns()


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

# MAIN LIST MANAGEMENT AND CLEANING
def remove_duplicates_from_incoming():
    # Removes duplicates from 'incoming',
    # returns ammount of URLs removed.
    # Only use when 'incoming_link_queue' is already loaded
    global incoming_url_list
    initial_length = len(incoming_url_list)
    incoming_url_list = list(dict.fromkeys(incoming_url_list))
    final_length = len(incoming_url_list)
    return initial_length - final_length
def removed_links_in_history_from_incoming():
    # Removes from 'incoming' URLs already present in 'history',
    # returns ammount of URLs removed
    # Only use when both lists are already loaded
    global incoming_url_list
    global url_history_list

    initial_length = len(incoming_url_list)
    incoming_url_list = [x for x in incoming_url_list
                         if x not in url_history_list]
    final_length = len(incoming_url_list)
    return initial_length - final_length
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
    duplicate_counter = remove_duplicates_from_incoming()
    existing_counter = removed_links_in_history_from_incoming()
    blacklisted_counter = remove_blacklisted_sites_from_incoming()

    removed_counter = (duplicate_counter
                       + existing_counter
                       + blacklisted_counter)
    
    print('\nRemoved {} pages:\n{} duplicates,\n{} existing\n{} blacklisted'
          .format(removed_counter, duplicate_counter,
                  existing_counter, blacklisted_counter))
    return removed_counter

# STATISTICS:
def count_pages_indexed():
    global url_history_list
    global redirector_flag
    load_history_from_file()
    real_indexed_list = [x for x in url_history_list if redirector_flag not in x]
    return len(real_indexed_list)

# CRAWLING
def pathfinder(ammount_to_search):
    # This function picks all links in a seed URL,
    # appends them to the 'incoming_url_list',
    # and does the same to the following URLs in the list
    # Searches the ammount of links defined in 'ammount_to_search'

    # For every valid link visited, its data pack will be saved to a list
    # so it can be indexed without having to extract the data again.
    # 'page_saver()' will gather the data of this list and index it.

    global seed_list

    global incoming_url_list
    global incoming_url_list_file

    global url_history_list
    global url_history_list_file


    global redirector_flag

    print('\nStart Run!')

    load_incoming_from_file() # Load 'incoming' list
    load_history_from_file() # Load 'history' list

    # If 'incoming' file is empty
    if incoming_url_list == []:
        # Add seed url to it
        plant_seed()
        save_incoming_to_file()

    # Limit how many items to comb through based on how many are available
    max_number_of_links = len(incoming_url_list)
    if ammount_to_search > max_number_of_links:
        ammount_to_search = max_number_of_links


    ###
    sample = incoming_url_list[:ammount_to_search]

    data_pack_bundle = []
    with Pool() as pool:
        data_pack_bundle = pool.map(save_website, sample, chunksize=5)
    pass
    ###


    # Found URLs go here before being appended to 'incoming' list
    intermediate_url_list = []
    current_url = ''
    old_url = ''
    #
    number_of_pages_searched = 0
    number_of_new_pages_found = 0
    while number_of_pages_searched < ammount_to_search:
        # Set up URL, get data
        current_url = incoming_url_list[0]

        #data_pack = save_website(current_url) # Indexes url and returns important data
        data_pack = data_pack_bundle[number_of_pages_searched] # Indexes url and returns important data
        

        old_url = data_pack[5]
        real_url = data_pack[6]
        intermediate_url_list.append(data_pack[7]) # Get link list

        # Print current URL
        display_url = textwrap.wrap(current_url, no_terminal_columns-1)
        print('{}'.format(display_url[0]))

        # Save to history
        if data_pack[4]:
            # If there was a redirection
            # Append searched_url with marker
            url_history_list.append(redirector_flag + old_url)
            # Append final_url unaltered
            url_history_list.append(real_url)

            # Print final URL
            print('REDIRECTED TO:')
            display_url = textwrap.wrap(real_url, no_terminal_columns-1)
            print('{}'.format(display_url[0]))

        else:
            # Just append it normally
            url_history_list.append(data_pack[6])
        
        number_of_pages_searched += 1
        # Remove current URL from queue
        incoming_url_list.pop(0)
    
    # Transfer all collected URLs in intermediate list to incoming
    for list in intermediate_url_list:
        for link in list:
            incoming_url_list.append(link)
            number_of_new_pages_found += 1

    # Clean 'incoming' before saving
    removed_counter = clean_incoming()
    number_of_new_pages_found -= removed_counter

    # Save 'incoming', 'history' and 'to_be_indexed'
    save_incoming_to_file()
    save_history_to_file()

    return number_of_pages_searched
def plant_seed():
    global incoming_url_list
    global seed_list
    global seed_list_file

    seed_list = load_list_from_file(seed_list_file)
    
    for seed in seed_list:
        incoming_url_list.append(seed)
    save_incoming_to_file()
# INTERFACE
def expand_index(number_to_expand):
    number_remaining = number_to_expand
    pages_searched = 0
    number_currently_found = 0

    # Limits each pathfinding so progress gets saved every x pages
    max_number_per_run = 100
    to_search  = 0

    start_time = time.perf_counter()
    while pages_searched < number_to_expand:
        if number_remaining > max_number_per_run:
            to_search = max_number_per_run
        else:
            to_search = number_remaining
        
        number_currently_found = pathfinder(to_search)
        pages_searched += number_currently_found
        number_remaining -= number_currently_found
        print('\nPages remaining: {}'.format(number_remaining))
    finish_time = time.perf_counter()

    print('{} pages added to index.'.format(pages_searched))

    total_seconds = finish_time - start_time
    seconds = round(total_seconds%60, 3)
    minutes = round((total_seconds//60)%60)
    hours = round(((total_seconds//60)//60)%24)
    days = round(((total_seconds//60)//60)//24)
    
    print('Task took {} days, {}:{}:{}'.format(days, hours, minutes, seconds))
    

    
    


# MAIN

def main():
    print('This is the Longin Crawler!')
    load_history_from_file()
    print('Ammount of pages currently indexed: {}'.format(count_pages_indexed()))
    while True:
        try:
            answer = int(input('How many pages do you want to index? '))
        except ValueError:
            print('Input a valid number!')
            continue
        expand_index(answer)
        break

    print('Ammount of pages currently indexed: {}'.format(count_pages_indexed()))
    input('Done! Press ENTER to exit')

# Multiprocessing tests
def multip_test_iteration(number_of_pages, chunk_size):
    # Does an iteration of the multiprocessing performance.
    # Choose how many pages to index and chunk size.
    # Returns number of pages indexed, time taken, and time per page

    global incoming_url_list
    load_incoming_from_file()

    sample = incoming_url_list[:number_of_pages]

    start_time = time.perf_counter()

    with Pool() as pool:
        result = pool.map(save_website, sample, chunksize=chunk_size)

    finish_time = time.perf_counter()
    time_taken = finish_time - start_time

    sample_length = len(sample)
    #print('Time taken: {}\nPages indexed: {}\nTime per page: {}'.format(time_taken, sample_length, time_taken/sample_length))
        
    return sample_length, time_taken/sample_length
def multiprocessing_statistics():
    # Executes many iterations automatically, as planned.
    # I have determined the best chunk size for sizes 100 forward is 5.
    # See "1 - multiprocessing test.ods"

    out_file = 'test_output.csv'

    # Steps to be permutated for the test
    number_of_pages_steps = [1, 5, 10, 50, 100, 500, 1000]
    chunk_size_steps = [1, 5, 10, 20, 50]

    #number_of_pages_steps = [1, 5, 10]
    #chunk_size_steps = [1, 5]

    # Names of the test results per iteration
    result_names = ['no_pages', 'time/page']
    


    chunk_results = []
    for css in chunk_size_steps:
        print('chunksize: {}'.format(css))
        result = []
        for nop in number_of_pages_steps:
            print('steps: {}'.format(nop))
            result.append(multip_test_iteration(nop, css))
        chunk_results.append(result)

    # Save data to file
    with open(out_file, 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)  

        for index, chunk in enumerate(chunk_results):
            writer.writerow(['chunksize: {}'.format(chunk_size_steps[index])])
            writer.writerow(result_names)
            
            for round in chunk:
                writer.writerow(round)
            writer.writerow([])


    pass

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
    #multiprocessing_statistics()




pass