# This script saves important data from the website and returns paths for the data.
import os
import website_data_extractor as site_ex

ALL_WEBSITES_FOLDER = 'SITES'

def main_folders_manager():
    global ALL_WEBSITES_FOLDER
    ALL_WEBSITES_FOLDER = os.path.join('.\\', ALL_WEBSITES_FOLDER)
    if(not os.path.exists(ALL_WEBSITES_FOLDER)):
        os.mkdir(ALL_WEBSITES_FOLDER)

def save_html_to_file(html, filepath):
   with open(filepath, 'wb') as file:
      file.write(html)

def save_list_to_file(list, path):
   with open(path, 'wb') as file:
    for index in range(len(list)):
        aux = list[index].encode('utf-8')
        file.write(aux)
        if index != len(list)-1:
            file.write(b'\n')


def website_path(name):
    aux = name
    #aux.append(name)
    if '/' in aux:
        aux = aux.split('/')
    aux.insert(0, ALL_WEBSITES_FOLDER)
    website_folder = aux[0]
    for level in range(len(aux)-1):
        website_folder = os.path.join(website_folder, aux[level+1])
        if(not os.path.exists(website_folder)):
            os.mkdir(website_folder)

    data_file = 'data.txt'
    data_file = os.path.join(website_folder, data_file)

    link_list_file = 'links.txt'
    link_list_file = os.path.join(website_folder, link_list_file)

    text_list_file = 'text.txt'
    text_list_file = os.path.join(website_folder, text_list_file)

    return data_file, link_list_file, text_list_file

def get_website(search_url):
    # Saves important data from the website, returns paths for the data.
    website_name, raw_file_data, link_list, text_list = site_ex.get_website_data(search_url)
    data_file, link_list_file, text_list_file = website_path(website_name)


    # Save data in folder
    save_html_to_file(raw_file_data, data_file) # Save raw html
    save_list_to_file(link_list, link_list_file) # Save links
    save_list_to_file(text_list, text_list_file) # Save text

    return data_file, link_list_file, text_list_file

main_folders_manager()
