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


MAIN_FOLDER = 'crawler_data'

incoming_url_list = []
incoming_url_list_file = 'queue.txt'

url_history_list = []
url_history_list_file = 'history.txt'

SEED_URL = 'https://en.wikipedia.org/wiki/Main_Page'


main_paths_manager()

def pathfinder():
    # This function picks all links in a seed URL,
    # appends them to the 'incoming_url_list',
    # and does the same to the following URLs in the list

    global SEED_URL
    global incoming_url_list
    global url_history_list

    aux = get_data_from_url()
    pass