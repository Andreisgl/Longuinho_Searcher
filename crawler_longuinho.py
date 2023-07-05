# This script crawls the web. It finds and downloads a webpage's raw data

import os

import urllib.request


test_folder = 'TESTE'
test_file = "teste.txt"

test_folder = os.path.join('.\\', test_folder)
test_file = os.path.join(test_folder, test_file)

if(not os.path.exists(test_folder)):
   os.mkdir(test_folder)




search_url = 'http://andreisegal.dev.br/'
with urllib.request.urlopen(search_url) as response:
   html = response.read()


with open(test_file, 'w') as file:
   data = html.decode('utf-8')
   file.write(data)






pass