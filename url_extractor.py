# This script downloads a webpage's raw data

import os
import urllib.request



# Folder management. Delete later, maybe move to the crawler







def extract_html(url):
   with urllib.request.urlopen(url) as response:
      html = response.read()
   return html

def save_html(html, filepath):
   with open(filepath, 'wb') as file:
      file.write(html)


#save_html(extract_html(search_url), data_file)



pass