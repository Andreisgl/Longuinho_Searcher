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


def main():
    main_folders_manager()

    auxlist = get_all_of_a_file_in_database(META_LIST_FILENAME)
    
    pass

# DATABASE INFO
PAGES_DATABASE_FOLDER = site_saver.get_pages_database_path()
DATA_FILENAME = ''
LINK_LIST_FILENAME = ''
TEXT_LIST_FILENAME = ''
META_LIST_FILENAME = ''






if __name__ == '__main__':
    main()