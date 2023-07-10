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


def main():
    main_folders_manager()
    
    pass

# DATABASE INFO
PAGES_DATABASE_FOLDER = site_saver.get_pages_database_path()
DATA_FILENAME = ''
LINK_LIST_FILENAME = ''
TEXT_LIST_FILENAME = ''
META_LIST_FILENAME = ''






if __name__ == '__main__':
    main()