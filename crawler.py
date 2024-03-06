# This script crawls a list of URLs, gets all links present in them
# and appends those to the list

import os
import shutil
from time import perf_counter

#import textwrap
from multiprocessing import Pool
#import csv

#from website_extractor import get_data_from_url
from site_saver import save_website

from modules import csv_methods as csvm


class Crawler:
    def __init__(self, root_dir):

        self.dir = root_dir
        
        self.MAIN_FOLDER = 'crawler_data'

        self.incoming_url_list = []
        self.incoming_url_list_file = 'input.csv'

        self.url_history_list = []
        self.url_history_list_file = 'history.csv'

        self.output_url_list = []
        self.output_url_list_file = 'output.csv'

        self.seed_list = []
        self.seed_list_file = 'seeds.csv'

        self.blacklist_list = []
        self.blacklist_list_file = 'blacklist.csv'

    # ENCAPSULATION
    # TODO: Move seeds and blacklist to node manager
        # Consider moving only history file to node manager as well
            # No. Async history transmission is necessary.
    # INPUT
    def get_input_path(self):
        '''Retrieve path to input file'''
        return self.incoming_url_list_file
    def get_input_data(self):
        '''Retrieve input data'''
        return self.load_incoming_from_file()
    def write_input_data(self, overwrite=True):
        '''Write input data
        - overwrite: If 'True', overwrites file
            If 'False', appends to file.
            Defaults 'True'.'''


    # MAIN PATHS MANAGER
    def main_paths_manager(self):
        '''This function creates and completes the paths
        for important files and folders'''
        
        def check_file(path):
            # Creates file it it does not exis already
            if not os.path.exists(path): # Create file if it does not exist
                with open(path, 'w'):
                    pass

        def check_folder(path):
            # Creates folder it it does not exis already
            if not os.path.exists(path):
                os.mkdir(path)

        # Main folder
        self.MAIN_FOLDER = os.path.join(self.dir, self.MAIN_FOLDER)
        check_folder(self.MAIN_FOLDER)

        # incoming_url_list_file
        self.incoming_url_list_file = os.path.join(self.MAIN_FOLDER, self.incoming_url_list_file)
        check_file(self.incoming_url_list_file)

        # url_history_list_file
        self.url_history_list_file = os.path.join(self.MAIN_FOLDER, self.url_history_list_file)
        check_file(self.url_history_list_file)

        # output_url_list
        self.output_url_list_file = os.path.join(self.MAIN_FOLDER, self.output_url_list_file)
        check_file(self.output_url_list_file)
        
        #seed_list_file
        self.seed_list_file = os.path.join(self.MAIN_FOLDER, self.seed_list_file)
        check_file(self.seed_list_file)
        
        #blacklist_list_file
        self.blacklist_list_file = os.path.join(self.MAIN_FOLDER, self.blacklist_list_file)
        check_file(self.blacklist_list_file)

    # LIST SAVING MANAGEMENT
    def save_list_in_file(self, in_list, filepath, many_rows=True, mode='w'):
        '''Saves a list as lines in a file
        Returns 'True' if succeeded, 'False' if failed.'''

        write_data = [(x,) for x in in_list]
        try:
            csvm.write_csv(filepath, write_data, many_rows, mode)
            return True
        except:
            return False
    def load_list_from_file(self, file_path):
        '''Returns a list containing all lines in a file'''
        data = csvm.read_csv(file_path)
        data = [x[0] for x in data]
        return data

    # INCOMING LIST MANAGEMENT
    def save_incoming_to_file(self):
        '''Saves 'incoming_url_list' to its respective file'''
        self.save_list_in_file(self.incoming_url_list, self.incoming_url_list_file)
    def load_incoming_from_file(self):
        '''Saves 'incoming_url_list' from its respective file'''
        self.incoming_url_list = self.load_list_from_file(self.incoming_url_list_file)
        if self.incoming_url_list == '':
            self.incoming_url_list = []

    # OUTPUT LIST MANAGEMENT
    def save_output_to_file(self):
        '''Saves 'incoming_url_list' to its respective file'''
        self.save_list_in_file(self.output_url_list, self.output_url_list_file)
    def load_output_from_file(self):
        '''Saves 'incoming_url_list' from its respective file'''
        self.output_url_list = self.load_list_from_file(self.output_url_list_file)
        if self.output_url_list == '':
            self.output_url_list = []

    # HISTORY LIST MANAGEMENT
    def save_history_to_file(self):
        '''Saves 'history_list' to its respective file'''
        history_header = ('URL', 'SUCCESS', 'REDIRECTOR')
        data_write = self.url_history_list[:]
        data_write.insert(0, history_header)
        csvm.write_csv(self.url_history_list_file, data_write, True)
    def load_history_from_file(self):
        '''Saves 'history_list' from its respective file'''
        self.url_history_list = list(csvm.read_csv(self.url_history_list_file))[1:]
        if self.url_history_list == '':
            self.url_history_list = []

    # BLACKLIST LIST MANAGEMENT
    def load_blacklist_from_file(self):
        '''Saves 'history_list' from its respective file'''
        self.blacklist_list = self.load_list_from_file(self.blacklist_list_file)
        if self.blacklist_list == '':
            self.blacklist_list = []

    # LIST CLEANING
    def remove_duplicates_from_list(self, input_list):
        '''Returns the list without duplicates and ammount of entries removed.'''

        process_list = input_list # Assign to avoid reference passes
        initial_length = len(process_list)
        # Transforming to 'dictionary removes duplicates
        process_list = list(dict.fromkeys(process_list))
        final_length = len(process_list)

        return process_list, (initial_length - final_length)
    def remove_entries_from_another_list(self, target_list, tool_list):
        '''Returns the 'target_list' without 'tool_list' entries
        and ammount of entries removed.'''

        initial_length = len(target_list)

        target_set = set(target_list)
        tool_set = set(tool_list)

        final_set = target_set.difference(tool_set)
        final_list = list(final_set)
        
        final_length = len(final_list)

        return final_list, (initial_length - final_length)
    def remove_blacklisted_sites_from_list(self, target_list):
        '''Some sites just take too long to load, like the web.archive.
        Returns cleansed list and number of excluded terms.
        Only use when 'incoming_link_queue' is already loaded'''

        self.load_blacklist_from_file()

        process_list = target_list
        
        # Add prefixes to each website so they reflect their counterparts
        # in 'incoming'
        prefixes = ['', 'http://', 'https://']
        full_terms = []

        initial_length = len(process_list)

        for site in self.blacklist_list:
            for prefix in prefixes:
                full_terms.append(prefix + site)
        
        for index, url in enumerate(process_list):
            for site in full_terms:
                if url.startswith(site):
                    process_list.pop(index)
        
        final_length = len(process_list)

        return process_list, (initial_length - final_length)

    # INCOMING CLEANING
    def remove_duplicates_from_incoming(self):
        '''Removes duplicates from 'incoming',
        returns ammount of URLs removed.
        Only use when 'incoming_link_queue' is already loaded'''

        (self.incoming_url_list,
        amt_removed
        ) = self.remove_duplicates_from_list(self.incoming_url_list)
        
        return amt_removed
    def removed_links_in_history_from_incoming(self):
        '''Removes from 'incoming' URLs already present in 'history',
        returns ammount of URLs removed
        Only use when both lists are already loaded'''

        (self.incoming_url_list,
        amt_removed
        ) = self.remove_entries_from_another_list(self.incoming_url_list, self.url_history_list)

        return amt_removed
    def remove_blacklisted_sites_from_incoming(self):
        '''Some sites just take too long to load, like the web.archive.
        This allows to remove them from the incoming list.
        Returns number of excluded terms.
        Only use when 'incoming_link_queue' is already loaded'''
        self.load_incoming_from_file()

        (self.incoming_url_list,
        amt_removed
        ) = self.remove_blacklisted_sites_from_list(self.incoming_url_list)
        
        return amt_removed
        
    def clean_incoming(self):
        '''Unifies all cleaning methods into a single call
        Returns total ammount of URLs removed
        Only use when 'incoming_link_queue' is already loaded'''

        removed_counter = 0

        duplicate_counter = self.remove_duplicates_from_incoming()
        
        existing_counter = self.removed_links_in_history_from_incoming()

        blacklisted_counter = self.remove_blacklisted_sites_from_incoming()

        removed_counter = (duplicate_counter
                        + existing_counter
                        + blacklisted_counter)
        
        if False:
            print('\nINPUT:Removed {} pages:\n{} duplicates,\n{} existing\n{} blacklisted'
                .format(removed_counter, duplicate_counter,
                        existing_counter, blacklisted_counter))
        
        return removed_counter

    # OUTPUT CLEANING
    def clean_output(self):
        '''Returns total ammount of URLs removed'''

        removed_counter = 0

        (self.output_url_list, duplicate_counter
        ) =self.remove_duplicates_from_list(self.output_url_list)
        
        (self.output_url_list, existing_counter
        ) = self.remove_entries_from_another_list(self.output_url_list, self.url_history_list)

        (self.output_url_list, blacklisted_counter
        ) = self.remove_blacklisted_sites_from_list(self.output_url_list)

        removed_counter = (duplicate_counter
                        + existing_counter
                        + blacklisted_counter)
        
        if False:
            print('\nOUTPUT: Removed {} pages:\n{} duplicates,\n{} existing\n{} blacklisted'
                .format(removed_counter, duplicate_counter,
                        existing_counter, blacklisted_counter))
        
        return removed_counter

    # STATISTICS:
    def count_pages_crawled(self):
        '''Count how many pages in history'''
        self.load_history_from_file()
        real_indexed_list = self.url_history_list[:]

        amt_crawled = len(real_indexed_list)
        print('Ammount of pages already crawled: {}'.format(amt_crawled))
        return amt_crawled
    def count_pages_available(self):
        '''Count how many pages in incoming'''
        amt_available = len(self.incoming_url_list)
        
        print('URLs available: {}'.format(amt_available))
        return amt_available
    # CRAWLING
    def plant_seed(self):
        self.seed_list = self.load_list_from_file(self.seed_list_file)
        
        for seed in self.seed_list:
            self.incoming_url_list.append(seed)
        self.save_incoming_to_file()

    def pathfinder(self, input_list, output_list, history_list, amt_to_search=-1, parallel_search=True):
        '''Crawls a list, returns ammount of pages crawled
        and ammount of pages available to crawl.
        - input_list: List to be crawled
        - output_list: All URLs found in this crawl
        - history_list: All URLs ever crawled
        - parallel_search: If 'True', crawling will use multithreading.
            If 'False', crawling will be serial.
        '''

        amt_available = len(input_list)
        # Crawls are only saved after the pathfinder closes.
        # Max ammount of URLs per crawl.
        max_amt = 200 
        
        # Define ammount of URLs to crawl
        # Cap search to available number or the max ammount per crawl
        if amt_to_search <= 0 or amt_to_search > amt_available:
            amt_to_search = amt_available
        if amt_to_search > max_amt:
            amt_to_search = max_amt

        sample = input_list[:amt_to_search] # Search just this ammount
        
        # Bundle URL packages
        print('Start Bundling')
        data_pack_bundle = []
        if parallel_search:
            with Pool() as pool:
                data_pack_bundle = pool.map(save_website, sample, chunksize=5)
        else:
            for url in sample:
                data_pack_bundle.append(save_website(url))

        # Manage recovered data
        recovered_urls = [] # Will be passed on to 'output_list' later
        visited_urls_counter = 0 # Redirections count as URLs, so count them too!
        for pack in data_pack_bundle:
            success_flag = pack[0]
            was_redirected = pack[1]
            searched_url = pack[2]
            final_url = pack[3]
            found_urls = pack[4]

            # Recover URLs
            for rec_url in found_urls:
                recovered_urls.append(rec_url)
            # Add to history
            if was_redirected: # If there is a redirection, append origin link with a marker
                history_list.append(
                    (searched_url, success_flag, True)
                    )
                visited_urls_counter += 1 # Count redirector URL as visited too
            
            
            history_list.append(
                    (searched_url, success_flag, False)
                    )
            
            visited_urls_counter += 1 # Count URL as visited
            
            # Removed visited pages from 'input_list'
            del input_list[:amt_to_search]
            # Update ammount of links available
            amt_available = len(input_list)
            
            # Append recovered URLs to 'output_list'
            output_list += recovered_urls

        # Return number of crawled and available pages
        return visited_urls_counter, amt_available

    def expand_index(self, amt_to_search, cycle_data=False):
        '''Covers many pathfindings to crawl desired ammount of pages.
        Returns ammount of pages crawled and time to do so.'''
        
        def call_pathfinder():
            return self.pathfinder(self.incoming_url_list, self.output_url_list, self.url_history_list, amt_to_search)

        def feedback_data():
            #global incoming_url_list
            #global url_history_list
            #global output_url_list

            if cycle_data:
                # Transfer output data to input
                self.incoming_url_list += self.output_url_list
                self.output_url_list.clear()
                print('Outputted values moved to input!')

        
        start_time = perf_counter() # Start counting execution time

        amt_searched_total = 0 # Ammount searched in total
        amt_searched = 0 # Ammount searched in iteration
        amt_available = 1 # Start as > 0 to not trigger termination

        if amt_to_search <= 0: # This is a call to crawl all available pages
            amt_searched += call_pathfinder()
            feedback_data()

        print('Crawl cycle START')
        while (amt_searched_total < amt_to_search
        and amt_available > 0):
            amt_searched, amt_available = call_pathfinder()
            amt_to_search -= amt_searched
            amt_searched_total += amt_searched
            feedback_data()
        else:
            print('Crawl cycle END')
        
        
        end_time = perf_counter() # Stop counting execution time
        time_taken = end_time - start_time

        # Statistics:
        secs = time_taken
        mins = time_taken//60
        hrs = mins//60
        days = hrs//24

        secs %= 60
        mins %= 60
        hrs %= 24

        formatted_time = f'{days}-{hrs}:{mins}:{secs:2f}'
        print(f'\nCrawled {amt_searched} pages in {formatted_time}')
        if amt_searched > 0:
            divider = amt_searched
        else:
            divider = 1
        print(f'{time_taken/divider:2f}s per page')

        return amt_searched, time_taken



# MAIN
def main():
    print('This is the Longin Crawler!')
    
    crawler = Crawler('.')
    crawler.main_paths_manager()

    

    # Assign main lists
    # Load from main files
    crawler.load_incoming_from_file()
    crawler.load_output_from_file()
    crawler.load_history_from_file()

    # Clean input
    crawler.clean_incoming()

    # Show simple statistics
    crawler.count_pages_crawled()
    crawler.count_pages_available()

    if False:
        if len(incoming_url_list) <= 0:
            crawler.plant_seed()
    
    while True: # Input desired amount of pages to crawl
        try:
            answer = int(input('How many pages do you want to index? '))
        except ValueError:
            print('Input a valid number!')
            continue
        break

    crawler.expand_index(answer)
    
    
    # Move output to input
    crawler.clean_output()

    
    # Save main files
    crawler.save_incoming_to_file()
    crawler.save_output_to_file()
    crawler.save_history_to_file()

    # Show simple statistics
    crawler.count_pages_crawled()
    crawler.count_pages_available()
    

    input('Done! Press ENTER to exit')


if __name__ == '__main__':
    main()


pass