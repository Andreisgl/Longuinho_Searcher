# This script crawls a list of URLs, gets all links present in them
# and appends those to the list

import os
from website_extractor import get_data_from_url

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
    # Saves 'incoming_url_list' to its respective file
    global url_history_list
    global url_history_list_file
    save_list_in_file(url_history_list, url_history_list_file)
def load_history_from_file():
    # Saves 'incoming_url_list' from its respective file
    global url_history_list
    global url_history_list_file
    url_history_list = load_list_from_file(url_history_list_file)
    if url_history_list == '':
        url_history_list = []




def pathfinder(ammount_to_search):
    # This function picks all links in a seed URL,
    # appends them to the 'incoming_url_list',
    # and does the same to the following URLs in the list
    # Searches the ammount of links defined in 'ammount_to_search'

    # With the crawling path defined,
    # another function can follow the found path and
    # effectively index the pages

    global SEED_URL

    global incoming_url_list
    global incoming_url_list_file

    global url_history_list
    global url_history_list_file

    load_incoming_from_file() # Load 'incoming' list
    load_history_from_file() # Load 'history' list

    # Limit how many items to comb through base on how many are available
    max_number_of_links = len(incoming_url_list)
    if ammount_to_search > max_number_of_links:
        ammount_to_search = max_number_of_links

    
    # If 'incoming' file is empty
    if incoming_url_list == []:
        # Add seed url to it
        incoming_url_list.append(SEED_URL)
        save_incoming_to_file()
    
    # If the called link redirected to somewhere else,
    # Mark it so it is included in history,
    # but not counted as an indexed page
    redirector_flag = '´'

    # Found URLs go here before being appended to 'incoming' list
    intermediate_url_list = []
    current_url = ''
    number_of_pages_searched = 0
    while number_of_pages_searched < ammount_to_search:
        # Set up URL, get data
        current_url = incoming_url_list[0]
        data_pack = get_data_from_url(current_url)
        intermediate_url_list.append(data_pack[6])

        # Save to history
        if data_pack[1]:
            # If there was a redirection
            # Append searched_url with marker
            url_history_list.append(redirector_flag + data_pack[2])
            # Append final_url unaltered
            url_history_list.append(data_pack[3])
        else:
            # Just append it normally
            url_history_list.append(data_pack[3])
        
        number_of_pages_searched += 1
        # Remove current URL from queue
        incoming_url_list.pop(0)
    
    # Transfer all collected URLs in intermediate list to incoming
    for list in intermediate_url_list:
        for link in list:
            incoming_url_list.append(link)

    # Save incoming and history
    save_incoming_to_file()
    save_history_to_file()
    return number_of_pages_searched

MAIN_FOLDER = 'crawler_data'

incoming_url_list = []
incoming_url_list_file = 'queue.txt'

url_history_list = []
url_history_list_file = 'history.txt'

SEED_URL = 'https://en.wikipedia.org/wiki/Main_Page'


main_paths_manager()

aux = pathfinder(10)
pass