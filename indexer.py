# This script wil comb through the pages database and manipulate information
import os
from CRAWLER.SAVER import site_saver

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
    main_page_path_list = gather_all_paths_in_database()

# TERM SEARCHING
def search_term_in_list(search_term, in_list):
    # Returns items in 'in_list' that contain the 'search_term'
    return [x for x in in_list if search_term in x]
def search_list_in_page(search_term, path):
    # Returns lines in a file that contain the 'search_term'
    data = site_saver.load_list_from_file(path)
    return search_term_in_list(search_term, data)


# RANKED_URL_LIST
def get_url_ranking_from_database():
    # Ranks all pages by the ammount of times they are mentioned in the database
    # Returns URLs and the times cited in descending order
    global main_page_path_list
    global main_page_path_list_file

    
    mention_list = []
    mention_count_list = []

    page_counter = 0
    for page in main_page_path_list:
        link_list = site_saver.load_list_from_file(page[2])
        page_dir = page[0]
        
        for index, link in enumerate(link_list):
            # Index unique links
            if link not in mention_list:
                mention_list.append(link)
                mention_count_list.append(0)
            # Increase count for existing links
            else:
                location = mention_list.index(link)
                mention_count_list[location] += 1
            page_counter += 1
    
    # Make a list for all URLs, each item consisting of [URL, count, path]
    mention_list = [[x, mention_count_list[i], page_dir] 
                    for i, x in enumerate(mention_list)]
    # Order links from most cited to less cited
    mention_list = [x for mention_list,
                    x in
                    sorted(zip(mention_count_list,mention_list),reverse=True)]
    return mention_list

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
    global ranked_url_list
    ranked_url_list = get_url_ranking_from_database()


def main():   
    global main_page_path_list
    global main_page_path_list_file
    global ranked_url_list
    global ranked_url_list_file

    main_folders_manager()
    

    load_main_page_path_list()
    load_ranked_url_list()
    
    #update_ranked_url_list()
    #save_ranked_url_list()
    

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


if __name__ == '__main__':
    main()