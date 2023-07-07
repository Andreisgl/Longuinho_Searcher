# This script indexes websites, gets the links from it
# and puts them into a queue for further crawling

import os
import indexer as indexer

class EmptyListException(Exception):
    pass

def main_folder_manager():
    global CRAWLER_FOLDER
    CRAWLER_FOLDER = os.path.join('.\\', CRAWLER_FOLDER)
    if not os.path.exists(CRAWLER_FOLDER):
        os.mkdir(CRAWLER_FOLDER)

    global link_queue_file
    link_queue_file = os.path.join(CRAWLER_FOLDER, link_queue_file)

def get_links_from_url(url):
    link_list_file = indexer.get_website(url)[1]
    link_list = []
    try:
        with open(link_list_file, 'r') as file:
            try:
                link_list = (file.read()).split('\n')
                if (link_list[0] == ''):
                    raise EmptyListException
            except UnicodeDecodeError:
                    print('UnicodeDecode EXCEPTION!')
            except EmptyListException:
                print('EmptyListException EXCEPTION!')
    except FileNotFoundError:
            print('FileNotFoundError EXCEPTION!')
        
    return link_list

def save_incoming_queue_to_file():
    indexer.save_list_to_file(incoming_link_queue, link_queue_file)

def load_incoming_from_file():
    global incoming_link_queue
    while True:
        try:
            with open(link_queue_file, 'rb') as file:
                #data = str(file.read())
                data = (file.read()).decode('utf-8')
                if data == '':
                    raise EmptyListException
                incoming_link_queue = data.split('\n')
        except FileNotFoundError:
            plant_seed()
            continue
        except EmptyListException:
            plant_seed()
            continue
        break

def iterate_queue(number_of_items):
    # Goes through the list scraping all links from the first URL in the list,
    # appends discovered links into the end of the list,
    # and removes the current link from the current URL.
    global current_link_queue
    global incoming_link_queue
    intermediate_link_queue = []

    load_incoming_from_file()
    remove_blacklisted_sites()

    max_number = len(incoming_link_queue)
    if (number_of_items >= max_number) or (number_of_items == 0):
        number_of_items = max_number
    
    
    found_links = 0
    pages_searched = 0
    index = 0
    while (pages_searched < number_of_items):        
        aux_list = get_links_from_url(incoming_link_queue[index])# Possible bottleneck?

        print('{} of {} - {}'.format(pages_searched, number_of_items, incoming_link_queue[index]))

        ammount_of_links = len(aux_list)
        if ammount_of_links > 0:
            found_links += ammount_of_links
            for item in aux_list:
                current_link_queue.append(item)
            pages_searched += 1

        incoming_link_queue.pop(index)
        intermediate_link_queue = intermediate_link_queue + current_link_queue
        #incoming_link_queue = incoming_link_queue + current_link_queue
        current_link_queue.clear()
        index += 1
    
    incoming_link_queue = incoming_link_queue + intermediate_link_queue
    save_incoming_queue_to_file()
    
    
    print('Pages searched: {} out of {}\tPages found: {}'.format(pages_searched, number_of_items, found_links))
    return pages_searched

def remove_blacklisted_sites():
    # Some sites just take too long to index, like the web.archive.
    # This allows to remove it from the incoming list.

    # Only use when list is already loaded
    blacklist = ['web.archive.org', 'abclocal.go.com']
    prefixes = ['http://', 'https://']
    full_terms = []

    for url in blacklist:
        for prefix in prefixes:
            full_terms.append(prefix + url)

    #load_incoming_from_file()
    
    pop_counter = 0
    for i in range(len(full_terms)):
        for j in range(len(incoming_link_queue)-1, 0, -1):
            #incoming_link_queue.pop(delete_index_list[j])
            if incoming_link_queue[j].find(full_terms[i]) != -1:
                pop_counter += 1
                incoming_link_queue.pop(j)
    print(str(pop_counter) + ' entries removed')
    #save_incoming_queue_to_file()
    pass

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

expand_index(1, 10)


pass