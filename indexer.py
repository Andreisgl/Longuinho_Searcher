# This script wil comb through the pages database and manipulate information
import os
import site_saver

from multiprocessing import Pool

from collections import Counter

def main_folders_manager():
    # Creates and manages all necessary folders

    # DATABASE INFO
    global DATA_FILENAME
    global LINK_LIST_FILENAME
    global TEXT_LIST_FILENAME
    global META_LIST_FILENAME

    (DATA_FILENAME,
     LINK_LIST_FILENAME,
     TEXT_LIST_FILENAME,
     META_LIST_FILENAME) = site_saver.get_filenames()
    
    # MAIN FOLDER
    global INDEXER_FOLDER
    INDEXER_FOLDER = os.path.join(os.path.dirname(__file__), INDEXER_FOLDER)
    if not os.path.exists(INDEXER_FOLDER):
        os.mkdir(INDEXER_FOLDER)

    # main_page_path_list FILE
    global main_page_path_list_file
    main_page_path_list_file = os.path.join(INDEXER_FOLDER, main_page_path_list_file)

    # ranked_url_list FILE
    global ranked_url_list_file
    ranked_url_list_file = os.path.join(INDEXER_FOLDER, ranked_url_list_file)

def file_comber(curr_dir, file_name):
    # Recursively finds and returns paths for a file name in a directory
    # Get proper paths for every folder in current dir
    item_list = [os.path.join(curr_dir, x) for x in os.listdir(curr_dir)]
    folder_list = [x for x in item_list if os.path.isdir(x)]
    file_list = [x for x in item_list if os.path.isfile(x)]
    path_list = []

    if os.path.join(curr_dir, file_name) in file_list:
        path_list.append(os.path.join(curr_dir, file_name))

    if len(folder_list) != 0: # If there are more folders here
        for folder in folder_list:
            data = file_comber(folder, file_name)
            if type(data) == list:
                path_list += data
            else:
                path_list.append(data)
    return path_list


def get_all_of_a_file_in_database(file_name):
    # Finds recursively all instances of a file name in the database
    return file_comber(PAGES_DATABASE_FOLDER, file_name)
def get_file_name_in_folder(file_name, folder):
    folder = os.path.dirname(folder)
    aux_list = []
    if file_name in os.listdir(folder):
        return os.path.join(folder, file_name)
    return ''
    


# LIST CONVERSION
def list_of_lists_to_saveable_list(input_list):
    # Some lists can't be writen to a file line by line,
    # as it is with such as 'main_page_path_list' and 'ranked_url_list'.

    # This function concatenates the contents of the sublist, separated by
    # a specific character,
    # and turns it into a simple list.

    # NOTE: This only works with a simple list of lists, in the format:
    # list[['a', 'b', 'c'], ['d', 'e', 'f']]
    # Result: ['a|b|c', 'd|e|f']
    
    # If a int type is present in the sublist,
    # it will be marked with an identifier

    separation_char = ('|')
    int_identifier = '´'

    simple_list = []

    for item in input_list:
        substring = ''
        for index, path in enumerate(item): # Another loop trick! I like it!
            # If subitem is int, mark it with an identifier
            if type(path) == int:
                path = int_identifier + str(path)
            substring += path
            if not index == len(item)-1:
                substring += separation_char
        simple_list.append(substring)

    return simple_list
def unpack_list_of_lists(input_list):
    # This function does the opposite of 'list_of_lists_to_saveable_list()'
    # Returns the layered list in its original state

    separation_char = ('|')
    int_identifier = '´'

    output_list = []
    for page in input_list:
        data = page.split('|')
        for index, subitem in enumerate(data):
            if int_identifier in subitem:
                data[index] = int(subitem.split(int_identifier)[1])
        output_list.append(data)

    return output_list


# MAIN_PAGE_PATH_LIST
def gather_all_paths_in_database():
    # Returns a list of all file paths for all pages
    global DATA_FILENAME
    global LINK_LIST_FILENAME
    global TEXT_LIST_FILENAME
    global META_LIST_FILENAME

    # Through meta files, we can locate every page without directory wizardry.
    file_name_list = [DATA_FILENAME, LINK_LIST_FILENAME, TEXT_LIST_FILENAME]

    meta_list = get_all_of_a_file_in_database(META_LIST_FILENAME)
    main_page_path_list = [[x] for x in meta_list]
    
    # Make elements of 'main_page_path_list' lists containing all four file paths
    for name in file_name_list:
        for page in main_page_path_list:
            page.append(get_file_name_in_folder(name, page[0]))
            # I really didn't know you could append directly like this. Yay!
    return main_page_path_list

def save_main_page_path_list():
    global main_page_path_list
    global main_page_path_list_file

    data = list_of_lists_to_saveable_list(main_page_path_list)
    
    site_saver.save_list_to_file(data, main_page_path_list_file)
def load_main_page_path_list():
    global main_page_path_list
    global main_page_path_list_file

    list = site_saver.load_list_from_file(main_page_path_list_file)
    main_page_path_list = unpack_list_of_lists(list)
def update_main_page_path_list():
    global main_page_path_list
    print('Update MPL')
    main_page_path_list = gather_all_paths_in_database()
    save_main_page_path_list()

# TERM SEARCHING
def search_term_in_list(search_term, in_list):
    # Returns items in 'in_list' that contain the 'search_term'
    return [x for x in in_list if search_term in x]
def search_list_in_page(search_term, path):
    # Returns lines in a file that contain the 'search_term'
    data = site_saver.load_list_from_file(path)
    return search_term_in_list(search_term, data)

def full_search_in_page(search_term, path):
    # Returns more complete data for a search in a page.
    # Bases search by meta_file, not text_file
    # It can accept any of the page's files as a valid path.
    
    # Get info from page
    page_base_dir = os.path.dirname(path)
    meta_path = os.path.join(page_base_dir, META_LIST_FILENAME)
    text_path = os.path.join(page_base_dir, TEXT_LIST_FILENAME)
    url = (site_saver.load_list_from_file(meta_path)[0]).split('\\')[1]

    # Search for term in text file
    aux = [search_list_in_page(search_term, text_path), url, meta_path]
    return aux

def search_term_in_ranked_database(search_term):
    # Search depending on relevance
    global ranked_url_list

    results = []

    sample = ranked_url_list
    # Prepare sample list with correct arguments
    # Since 'search_term' is an argument, it must appear in all items.
    # That's how 'pool.starmap()' works!
    sample = [[search_term, x[1]] for x in sample]

    # Search all pages with multiprocessing.
    data_pack_bundle = []
    with Pool() as pool:
        data_pack_bundle = pool.starmap(full_search_in_page, sample, chunksize=5)
    # Rid bundle from instances with no results
    data_pack_bundle = [x for x in data_pack_bundle if x[0] != []]

    
    return data_pack_bundle

# RANKED_URL_LIST
def get_url_ranking_from_database():
    # Ranks pages by the ammount of times they are mentioned in the database
    # Returns [URL, meta file path, times cited] in descending order.
    global main_page_path_list
    global main_page_path_list_file

    print('Ranking URLs')

    # Get all links possible in all indexed pages
    all_links = []

    sample = main_page_path_list # Workset to work with

    link_list_paths = [x[2] for x in sample] # Get all link files' paths
    pages_work_set = []
    # Reduce sample list to [URL, meta_file_path]
    for page in sample:
        meta_path = page[0]
        page_link = (site_saver.load_list_from_file(meta_path)[0]).split('\\')[1]
        pages_work_set.append([page_link, meta_path])
    
    # Collect the contents of all link files with multiprocessing
    data_pack_bundle = []
    with Pool() as pool:
        data_pack_bundle = pool.map(site_saver.load_list_from_file, link_list_paths, chunksize=5)
    
    # Put all link from bundles in a simple, single list.
    for page in data_pack_bundle:
        for link in page:
            all_links.append(link)

    # Count all obtained links
    count_list = Counter(all_links)

    # Create list of all links obtained, without duplicates.
    #all_unique_links = set(all_links) # Is this redundant, with the 'sample' list?
    #pages_work_set

    # Assemble list of every link and their score
    full_mention_list = [[x[0], x[1], count_list[x[0]]] for x in pages_work_set]
    
    full_mention_list.sort(key=lambda full_mention_list: full_mention_list[2], reverse=True)
    
    # Strip score from list
    #page_link_rank = [x[0] for x in full_mention_list]
    page_link_rank = full_mention_list
    
    print('URLs ranked!')
    return page_link_rank

def save_ranked_url_list():
    global ranked_url_list
    global ranked_url_list_file

    data = list_of_lists_to_saveable_list(ranked_url_list)
    site_saver.save_list_to_file(data, ranked_url_list_file)
def load_ranked_url_list():
    global ranked_url_list
    global ranked_url_list_file

    list = site_saver.load_list_from_file(ranked_url_list_file)
    ranked_url_list = unpack_list_of_lists(list)
def update_ranked_url_list():
    # The rank of the currently indexed pages
    global ranked_url_list

    update_main_page_path_list()
    save_main_page_path_list()
    
    print('Update RUL')
    ranked_url_list = get_url_ranking_from_database()

    save_ranked_url_list()

# Search


def main():   
    global main_page_path_list
    global main_page_path_list_file
    global ranked_url_list
    global ranked_url_list_file
    
    load_main_page_path_list()
    load_ranked_url_list()
    
    if False:
        update_ranked_url_list()
    
    search_term = 'plane'
    result = search_term_in_ranked_database(search_term)
    

    pass



# DATABASE INFO
PAGES_DATABASE_FOLDER = site_saver.get_pages_database_path()
DATA_FILENAME = ''
LINK_LIST_FILENAME = ''
TEXT_LIST_FILENAME = ''
META_LIST_FILENAME = ''

INDEXER_FOLDER = 'INDEXER'

main_page_path_list_file = 'INDEXER_MPL.txt'
main_page_path_list = []

ranked_url_list = []
ranked_url_list_file = 'INDEXER_URL_rank.txt'

main_folders_manager()

if __name__ == '__main__':
    main()