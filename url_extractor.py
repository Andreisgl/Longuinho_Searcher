# This script downloads a webpage's raw data

import os
import urllib.request

def extract_html(url):
   with urllib.request.urlopen(url) as response:
      html = response.read()
   return html