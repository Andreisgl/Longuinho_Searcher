# This script crawls the web. It finds and downloads a webpage's raw data

import os
import urllib.request

def sanitize_url_to_name(input):
   removal_list = ['http://', 'https://', 'www.']
   
   output = input
   for item in removal_list:
      output = output.replace(item, '')
   
   if output[-1] == '/':
      output = output[:-1]

   return output

ALL_WEBSITES_FOLDER = 'SITES'
ALL_WEBSITES_FOLDER = os.path.join('.\\', ALL_WEBSITES_FOLDER)

search_url = 'http://hashomer.org.br/'

website_name = sanitize_url_to_name(search_url)

website_folder = ''
website_folder = os.path.join(ALL_WEBSITES_FOLDER, website_name)



data_file = "data.txt"
data_file = os.path.join(website_folder, data_file)


if(not os.path.exists(ALL_WEBSITES_FOLDER)):
   os.mkdir(ALL_WEBSITES_FOLDER)

if(not os.path.exists(website_folder)):
   os.mkdir(website_folder)




with urllib.request.urlopen(search_url) as response:
   html = response.read()


with open(data_file, 'w') as file:
   data = html.decode('ascii', 'ignore')
   file.write(data)






pass