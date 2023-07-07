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

    global link_history_file
    link_history_file = os.path.join(CRAWLER_FOLDER, link_history_file)

def get_links_from_url(url):
    link_list_file = indexer.get_website(url)[1]
    link_list = []
    error_type = ''
    try:
        with open(link_list_file, 'r') as file:
            try:
                link_list = (file.read()).split('\n')
                if (link_list[0] == ''):
                    raise EmptyListException
            except UnicodeDecodeError:
                    error_type = 'UnicodeDecode EXCEPTION!'
            except EmptyListException:
                error_type = 'EmptyListException EXCEPTION!'
                link_list = []
    except FileNotFoundError:
            error_type = 'FileNotFoundError EXCEPTION!'
        
    return link_list, error_type

#LIST MANAGEMENT
def load_list_from_file(in_file, list):
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
    

#INCOMING_LINK_QUEUE
def save_incoming_queue_to_file():
    indexer.save_list_to_file(incoming_link_queue, link_queue_file)
def load_incoming_from_file():
    global link_history_file
    global incoming_link_queue
    while True:
        data = load_list_from_file(link_queue_file, incoming_link_queue)
        if data == FileNotFoundError:
            plant_seed()
            continue
        break
        #save_incoming_queue_to_file()
    return data

#HISTORY
def save_to_history(list_of_links):
    # Saves a list of links to the 'link_history_file'
    indexer.save_list_to_file(link_history_list, link_history_file)
def load_history_from_file(): #########TODO
    data = load_list_from_file(link_history_file, link_history_list)
    if data == FileNotFoundError or data == '':
        link_history_list.append(SEED_URL)
        with open(link_history_file, 'wb'):
            save_to_history(link_history_list)


#####
def iterate_queue(number_of_items):
    # Goes through the list scraping all links from the first URL in the list,
    # appends discovered links into the end of the list,
    # and removes the current link from the current URL.
    global current_link_queue
    global incoming_link_queue
    intermediate_link_queue = []

    load_incoming_from_file()
    load_history_from_file()

    max_number = len(incoming_link_queue)
    if (number_of_items >= max_number) or (number_of_items == 0):
        number_of_items = max_number
    
    
    found_links = 0
    pages_searched = 0
    index = 0
    while (pages_searched < number_of_items):        
        aux_list, url_error = get_links_from_url(incoming_link_queue[index])# Possible bottleneck?

        print('{} of {} - {}'.format(pages_searched+1, number_of_items, incoming_link_queue[index]))

        ammount_of_links = len(aux_list)
        if ammount_of_links > 0 and aux_list[0] != '': ##########
            found_links += ammount_of_links
            for item in aux_list:
                current_link_queue.append(item)
            pages_searched += 1
        else:
            print(url_error)

        incoming_link_queue.pop(index)

        # Save all pages found in this search
        intermediate_link_queue = intermediate_link_queue + current_link_queue

        current_link_queue.clear()
        index += 1
    
    # Before saving to history, remove duplicates!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    #save_to_history(intermediate_link_queue)###########################3

    # Add all found pages into 'incoming_link_queue'
    incoming_link_queue = incoming_link_queue + intermediate_link_queue
    
    removed_links = clean_incoming_links()
    save_incoming_queue_to_file()
    print('Iteration finished!')
    #print('''Pages searched: {} out of {}\tPages found: {} Pages removed: {}'''.format(pages_searched, number_of_items, found_links, removed_links))
    print('Pages searched: {} out of {}'.format(pages_searched, number_of_items))
    print('New pages found: ' + str(found_links + removed_links))
    return pages_searched

def remove_link_from_queue(term):
    # Removes links from 'incoming_queue', return ammount of terms removed.
    pop_counter = 0
    for j in range(len(incoming_link_queue)-1, 0, -1):
        if incoming_link_queue[j].find(term) != -1:
            pop_counter += 1
            incoming_link_queue.pop(j)
    return pop_counter
def remove_blacklisted_sites():
    # Some sites just take too long to index, like the web.archive.
    # This allows to remove it from the incoming list.
    # Returns number of excluded terms.
    # Only use when incoming_link_queue is already loaded
    blacklist = ['web.archive.org', 'abclocal.go.com']
    prefixes = ['http://', 'https://']
    full_terms = []
    remove_counter = 0

    for url in blacklist:
        for prefix in prefixes:
            full_terms.append(prefix + url)
    for term in full_terms:
        remove_link_from_queue(term)
    return remove_counter
    #pop_counter = 0
    #for i in range(len(full_terms)):
        #for j in range(len(incoming_link_queue)-1, 0, -1):
            
            #if incoming_link_queue[j].find(full_terms[i]) != -1:
                #pop_counter += 1
                #incoming_link_queue.pop(j)
    #print(str(pop_counter) + ' entries removed')

def remove_duplicated_sites():
    # This function removes duplicates from the incoming list.
    # Returns number of excluded terms.
    # Only use when incoming_link_queue is already loaded
    global incoming_link_queue

    initial_size = len(incoming_link_queue)
    incoming_link_queue = list(dict.fromkeys(incoming_link_queue))
    final_size = len(incoming_link_queue)
    
    return initial_size - final_size

def clean_incoming_links():
    # This function rids 'incoming_link_queue' from:
    # Duplicated websites and
    # Blacklisted websites.
    # Returns the total ammount of websites eliminated.
    
    removed_duplicate_counter = remove_duplicated_sites()
    removed_blacklist_counter = remove_blacklisted_sites()
    print('''Removed {} duplicates and {} blacklisted websites.
    '''.format(removed_duplicate_counter, removed_blacklist_counter))

    return removed_duplicate_counter + removed_blacklist_counter



CRAWLER_FOLDER = 'CRAWLER'
link_queue_file = 'link_queue.txt'
link_history_file = 'link_history.txt'

incoming_link_queue = []
link_history_list = []


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
    print('Expanded index by {} iterations, {} links.'.format(number_of_iterations, max_urls_per_iteration))

#plant_seed()

expand_index(1, 10)




pass