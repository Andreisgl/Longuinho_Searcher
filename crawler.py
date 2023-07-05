# This script indexes websites, gets the links from it
# and puts them into a queue for further crawling

import os
import indexer as indexer

SEED_URL = 'hashomer.org.br'

link_list_file = indexer.get_website(SEED_URL)[1]
with open(link_list_file, 'r') as file:
    link_list = (file.read()).split('\n')


pass