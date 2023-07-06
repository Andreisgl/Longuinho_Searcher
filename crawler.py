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

def save_current_link_queue_to_file():
    indexer.save_list_to_file(current_link_queue, link_queue_file)

def move_current_queue_to_incoming():
    incoming_link_queue = current_link_queue.copy()

CRAWLER_FOLDER = 'CRAWLER'
link_queue_file = 'link_queue.txt'
main_folder_manager()


SEED_URL = 'hashomer.org.br'
current_link_queue = []
incoming_link_queue = []

incoming_link_queue.append(SEED_URL)


for link in incoming_link_queue:
    aux_list = []
    list_path = indexer.get_website(link)[1]
    with open(list_path, 'r') as file:
        aux_list = (file.read()).split('\n')
    for item in aux_list:
        current_link_queue.append(item)
    incoming_link_queue.clear()
    incoming_link_queue = current_link_queue.copy()

# Go through incoming CHECK
# Add all links obtained in incoming to current CHECK
# clear incoming CHECK
# move current to incoming



pass