# This script indexes websites, gets the links from it
# and puts them into a queue for further crawling

import os
import indexer as indexer


def main_folder_manager():
    global CRAWLER_FOLDER
    CRAWLER_FOLDER = os.path.join('.\\', CRAWLER_FOLDER)
    if not os.path.exists(CRAWLER_FOLDER):
        os.mkdir(CRAWLER_FOLDER)

    global link_queue_file
    link_queue_file = os.path.join(CRAWLER_FOLDER, link_queue_file)

def get_links_from_url(url):
    link_list_file = indexer.get_website(url)[1]
    with open(link_list_file, 'r') as file:
        link_list = (file.read()).split('\n')
    return link_list

def save_incoming_queue_to_file():
    indexer.save_list_to_file(incoming_link_queue, link_queue_file)

def load_incoming_from_file():
    global incoming_link_queue
    with open(link_queue_file, 'r') as file:
        incoming_link_queue = (file.read()).split('\n')

def iterate_queue(number_of_items):
    global current_link_queue
    global incoming_link_queue

    load_incoming_from_file()

    max_number = len(incoming_link_queue)
    if (number_of_items >= max_number) or (number_of_items == 0):
        number_of_items = max_number
    
    
    
    for link in range(number_of_items):
        aux_list = []
        list_path = indexer.get_website(incoming_link_queue[link])[1]

        print(incoming_link_queue[link])

        try:
            with open(list_path, 'r') as file:
                try:
                    aux_list = (file.read()).split('\n')
                    for item in aux_list:
                        current_link_queue.append(item)
                except UnicodeDecodeError:
                    print('UnicodeDecode EXCEPTION!')
        except FileNotFoundError:
            pass
        
        incoming_link_queue.pop(link)
        incoming_link_queue = incoming_link_queue + current_link_queue
        current_link_queue.clear()

        save_incoming_queue_to_file()
    
    number_found = len(aux_list)
    print('Pages searched: {}\tPages found: {}'.format(number_of_items, number_found))

CRAWLER_FOLDER = 'CRAWLER'
link_queue_file = 'link_queue.txt'
main_folder_manager()


SEED_URL = 'https://en.wikipedia.org/wiki/English_Wikipedia'


current_link_queue = []
incoming_link_queue = []

def plant_seed():
    # Runs a single iteration from the seed URL
    incoming_link_queue.append(SEED_URL)
    save_incoming_queue_to_file()

    number_of_iterations = 1
    for iteration in range(number_of_iterations):
        iterate_queue(0)
    print('Seed planted!')



def expand_index(number_of_iterations, max_urls_per_iteration):
    for iteration in range(number_of_iterations):
        iterate_queue(max_urls_per_iteration)
    print('Expanded index: {} iterations, {} links.'.format(number_of_iterations, max_urls_per_iteration))

#plant_seed()
expand_index(1, 49)
pass