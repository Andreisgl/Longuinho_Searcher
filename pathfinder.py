'''This script crawls a list of URLs, gets all links present in them
and appends those to the list'''

import os

from time import perf_counter
from multiprocessing import Pool
from site_saver import PageSaver


def pathfinder(input_list, pg_svr:PageSaver, parallel_search=True):
    '''Crawls a list, returns ammount of pages crawled
    and ammount of pages available to crawl.
    - input_list: List to be crawled
    - output_list: All URLs found in this crawl
    - history_list: All URLs crawled in this iteration
    - parallel_search: If 'True', crawling will use multithreading.
        If 'False', crawling will be serial.
    '''

    workset = input_list
    
    # Bundle URL packages
    print('Start Bundling')
    data_pack_bundle = []
    if parallel_search:
        with Pool() as pool:
            data_pack_bundle = pool.map(pg_svr.save_website, workset, chunksize=5)
    else:
        for url in workset:
            data_pack_bundle.append(pg_svr.save_website(url))

    # Manage recovered data
    internal_history = []
    recovered_urls = []
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
            internal_history.append((searched_url, success_flag, True))
            visited_urls_counter += 1 # Count redirector URL as visited too
        
        display_url = final_url
        if not success_flag:
            display_url = searched_url
        internal_history.append((display_url, success_flag, False))
        visited_urls_counter += 1 # Count URL as visited

    # Return number of crawled and available pages
    return visited_urls_counter, recovered_urls, internal_history

def expand_index(input_list, pg_svr:PageSaver, amt_to_search=0):
    '''Covers many pathfindings to crawl desired ammount of pages.
    Returns ammount of pages crawled and time to do so.'''
        
    start_time = perf_counter() # Start counting execution time

    amt_searched_total = 0 # Ammount searched in total
    amt_searched = 0 # Ammount searched in iteration
    amt_available = len(input_list) # Start as > 0 to not trigger termination

    # This is a call to crawl all available URLs at once
    crawl_set = []
    if amt_to_search <= 0 or amt_to_search > amt_available: 
        crawl_set = input_list[:]
    else:
        crawl_set = input_list[:amt_to_search]
    
    returned_data = pathfinder(crawl_set, pg_svr, amt_to_search)
    amt_searched = returned_data[0]
    output_list = returned_data[1]
    history_list = returned_data[2]

    amt_searched_total += amt_searched


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

    divider = 1 # Avoid dividing by zero
    if amt_searched != 0:
        divider = amt_searched
    print(f'\nCrawled {amt_searched} pages in {formatted_time}')
    print(f'{time_taken/divider:2f}s per page')

    return output_list, history_list, amt_searched, time_taken

