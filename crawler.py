# This script indexes websites, gets the links from it
# and puts them into a queue for further crawling

import os
import shutil
import textwrap

from CRAWLER.SAVER import site_saver as site_saver

cdw = os.getcwd()
pass
# EXCEPTIONS
class EmptyListException(Exception):
    pass

# DISPLAY STUFF
def get_terminal_columns():
    return shutil.get_terminal_size().columns
no_terminal_columns = get_terminal_columns()

# PATH MANAGEMENT
def main_folder_manager():
    global CRAWLER_FOLDER
    CRAWLER_FOLDER = os.path.join(os.path.dirname(__file__),
                                  'CRAWLER', CRAWLER_FOLDER)
    if not os.path.exists(CRAWLER_FOLDER):
        os.mkdir(CRAWLER_FOLDER)

    global link_queue_file
    link_queue_file = os.path.join(CRAWLER_FOLDER, link_queue_file)

    global link_history_file
    link_history_file = os.path.join(CRAWLER_FOLDER, link_history_file)

# LINK EXTRACTION
def get_links_from_url(url):
    website_paths = site_saver.get_website(url)
    website_paths = website_paths[0:2]+website_paths[3:4]
    link_list_file, meta_list_file = website_paths[1:] # Data, link, text.
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
            # Check if it just has no links or is not indexed at all
            try:
                with open(meta_list_file, 'r'):
                    pass
                # If meta_list_file opens, it just has no links
                error_type = 'No links in this site!'
            except FileNotFoundError:
                    # If it does not exist, it is not indexed at all
                    error_type = 'Site not indexed'
        
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
    site_saver.save_list_to_file(incoming_link_queue, link_queue_file)
def load_incoming_from_file():
    global link_queue_file
    global incoming_link_queue
    while True:
        data = load_list_from_file(link_queue_file, incoming_link_queue)
        if data == FileNotFoundError:
            plant_seed()
            continue
        incoming_link_queue = data
        break
    return data

#HISTORY
def save_to_history():
    # Saves a list of links to the 'link_history_file'
    site_saver.save_list_to_file(link_history_list, link_history_file)
    pass
def load_history_from_file():
    global link_history_list
    link_history_list = load_list_from_file(link_history_file, link_history_list)
    if link_history_list == FileNotFoundError or link_history_list == '':
        link_history_list = []
        with open(link_history_file, 'wb'):
            pass

# LIST CLEANING
def remove_all_instances_in_list(term, list):
    pop_counter = 0
    for j in range(len(list)-1, 0, -1):
        if list[j].find(term) != -1:
            pop_counter += 1
            list.pop(j)
    return pop_counter
def remove_link_from_incoming_queue(term):
    # Removes links from 'incoming_queue', return ammount of terms removed.
    pop_counter = 0
    remove_all_instances_in_list(term, incoming_link_queue)
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
        remove_link_from_incoming_queue(term)
    return remove_counter
def remove_duplicated_sites():
    # This function removes duplicates from the incoming list.
    # Returns number of excluded terms.
    # Only use when incoming_link_queue is already loaded
    global incoming_link_queue

    initial_size = len(incoming_link_queue)
    #incoming_link_queue = list(dict.fromkeys(incoming_link_queue))
    incoming_link_queue = remove_duplicates_from_list(incoming_link_queue)
    final_size = len(incoming_link_queue)
    
    return initial_size - final_size
def remove_duplicates_from_list(in_list):
    in_list = list(dict.fromkeys(in_list))
    return in_list
def remove_links_in_history_from_incoming():
    # Removes from 'incoming' links already present in history.
    global incoming_link_queue
    links_removed = 0
    starting_ammount = len(incoming_link_queue)

    i = 0
    while True:
        if i <= len(link_history_list)-1:
            break
        inc = incoming_link_queue[i]
        for h in range(len(link_history_list)):
            his = link_history_list[h]
            if inc == his:
                incoming_link_queue.pop(i)
            else:
                i += 1
    links_removed = starting_ammount - len(incoming_link_queue)
    return links_removed
def clean_incoming_links():
    # This function rids 'incoming_link_queue' from:
    # Duplicated websites,
    # Blacklisted websites
    # and websites already present in history
    # Returns the total ammount of websites eliminated.
    
    removed_duplicate_counter = remove_duplicated_sites()
    removed_blacklist_counter = remove_blacklisted_sites()
    removed_existent_counter = remove_links_in_history_from_incoming()
    
    total_removed = removed_duplicate_counter + removed_blacklist_counter + removed_existent_counter

    final_statistics = (
        'Removed {} duplicates, {} blacklisted, {} already indexed websites.'
        ).format(removed_duplicate_counter, removed_blacklist_counter,
        removed_existent_counter)
    
    print(final_statistics)
    print('Total removed: ' + str(total_removed))

    return total_removed

# CRAWLING
def plant_seed():
    # Runs a single iteration from the seed URL
    incoming_link_queue.append(SEED_URL)
    save_incoming_queue_to_file()
    print('Seed planted!')
# MAIN ITERATOR - TODO: Make function to iterate history folder for reindexing
def crawl_queue(number_of_items):
    # Goes through 'incoming'
    # scrapes all links from the first URL in the list,
    # appends discovered links into the end of the list,
    # removes the current link from the current URL,
    # and proceeds to the next URL in 'incoming'
    global current_link_queue
    global incoming_link_queue
    intermediate_link_queue = []
    global link_history_list

    print ('START Iteration')
    load_incoming_from_file()
    load_history_from_file()

    max_number = len(incoming_link_queue)
    if (number_of_items >= max_number) or (number_of_items == 0):
        number_of_items = max_number
    
    
    found_links = 0
    pages_searched = 0
    while (pages_searched < number_of_items):
        # Print current URL
        display_url = textwrap.wrap(incoming_link_queue[0], no_terminal_columns)
        print('{}'.format(display_url[0]))
        
        # Keep doing normal stuff
        aux_list, url_error = get_links_from_url(incoming_link_queue[0])# Possible bottleneck?

        ammount_of_links = len(aux_list)
        if ammount_of_links > 0 and aux_list[0] != '':
            found_links += ammount_of_links
            for item in aux_list:
                current_link_queue.append(item)
            pages_searched += 1
        else:
            print(url_error)

        # Save current link to history, if page is indexed
        if url_error != 'Site not indexed':
            link_history_list.append(incoming_link_queue[0])
        # Remove current link from incoming
        incoming_link_queue.pop(0)

        # Save all pages found in this search
        intermediate_link_queue = intermediate_link_queue + current_link_queue

        current_link_queue.clear()
    

    # Add all found pages into 'incoming_link_queue'
    incoming_link_queue = incoming_link_queue + intermediate_link_queue
    
    # Clean 'incoming' before saving
    removed_links = clean_incoming_links()
    found_links = found_links - removed_links

    save_incoming_queue_to_file()
    save_to_history()
    
    # Data for output: pages_searched, number_of_items, found_links
    return pages_searched, number_of_items, found_links

CRAWLER_FOLDER = 'crawler_data'
link_queue_file = 'link_queue.txt'
link_history_file = 'link_history.txt'

incoming_link_queue = []
link_history_list = []


main_folder_manager()


SEED_URL = 'https://en.wikipedia.org/wiki/English_Wikipedia'


current_link_queue = []
incoming_link_queue = []





def expand_index(number_of_urls_to_expand):
    max_pages_per_iteration = 10
    number_of_iterations = 0
    total_pages_searched = 0
    remaining_number_to_search = number_of_urls_to_expand
    total_found_links = 0
    pages_to_search = 0

    while total_pages_searched < number_of_urls_to_expand:
        pages_to_search = remaining_number_to_search
        if remaining_number_to_search > max_pages_per_iteration:
            pages_to_search = max_pages_per_iteration
        (pages_searched, number_of_items,
            found_links) = crawl_queue(pages_to_search)
        
        number_of_iterations += 1
        total_pages_searched += pages_searched
        remaining_number_to_search -= pages_searched
        total_found_links += found_links

        print('\nIteration finished!')
        print('Pages searched: {} of {}\n'
            .format(pages_searched, number_of_urls_to_expand))
        #print('New pages found: {}\n'.format(str(found_links)))

    print('Expanded index by {} iterations, {} links.'.format(
        number_of_iterations, total_pages_searched))
    print('New pages found: {}'.format(total_found_links))
    pass

def main():
    print('Web crawler for Longin searcher')
    error_counter = 0
    while True:
        try:
            answer = int(input('Input how many webpages to index: '))
        except ValueError:
            error_counter += 1
            if error_counter >= 3:
                print('Input a number, dummy!')
            continue
        break
    expand_index(answer)


if __name__ == '__main__':
    main()