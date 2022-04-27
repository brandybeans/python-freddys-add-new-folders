import fileinput
import os
import shutil
import re
from time import sleep

''' Blank Staging File folder location '''
blank_staging_folder = r"\\192.168.1.100\map_as_y\Brink\Customers\FFC\pdill\Blank Staging File - Brink"

''' NAS folder location '''
network_drive_loc = "\\\\192.168.1.100\\map_as_y\\Brink\\Customers\\FFC\\Staging\\"
network_blank_staging_loc = "\\\\192.168.1.100\\map_as_y\\Brink\Customers\\FFC\\pdill\\Blank Staging File - Brink\\"

folders = [
        'R6',
        'R7',
        'R8',
        'R9',
        'Fryer',
        'Patio Expo',
        'Custard 2'
]

def get_loc_id_r1(r1):
    filename = r1
    file = open(filename, "r")
    line = file.read()
    regex = r"(\w\w\w\w\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\w\w\w\w\w\w\w\w)"
    regexsearch = re.search(regex, line)
    replacement_text = regexsearch[1]
    return replacement_text

def overwrite_text_in_file(text_to_search, replacement_text, dst):
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')

def get_kitchen_terminal_num(src):
    filename = src
    file = open(filename, "r")
    line = file.read()
    regex = re.search(r" (TerminalNumber=\"[1-9]*\")", line)
    replacement_text = regex[1]
    return replacement_text

storefolders = os.listdir(network_drive_loc)
print(storefolders)
for store in storefolders:
    #print("Updating store {}".format(store))
    if os.path.isfile(network_drive_loc+store+"\\R1\\Register.cfg"):
        try:
            r1 = network_drive_loc + store + "\\R1\\" + "Register.cfg"
            location_id = get_loc_id_r1(r1)
        except:
            print("Failed to get location_ID for {} in R1 Folder".format(store))
        for folder in folders:

            if not os.path.isdir(network_drive_loc+store+"\\"+folder):
                os.makedirs(network_drive_loc+store+"\\"+folder)
            if len(folder) == 2:
                src = blank_staging_folder + "\\R2\\Register.cfg"
                dst = network_drive_loc+store+ "\\" + folder + "\\" + "Register.cfg"
                r1 = network_drive_loc+store+ "\\R1\\" + "Register.cfg"
                if os.path.isfile(dst):
                    os.remove(dst)
                shutil.copy(src, dst)

                filename = dst
                file = open(filename, "r")
                line = file.read()
                file.close()
                regex = re.search(r" (TerminalNumber=\"[1-9]\")", line)
                replacement_text = "TerminalNumber=\"" + folder[1] + "\""
                try:
                    text_to_search = regex[1]
                    overwrite_text_in_file(text_to_search, replacement_text, dst)
                except:
                    print("Issue with {}".format(store))

                filename = dst
                file = open(filename, "r")
                line = file.read()
                file.close()
                regex2 = r"(\w\w\w\w\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\w\w\w\w\w\w\w\w)"
                regexsearch2 = re.search(regex2, line)
                try:
                    text_to_search = regexsearch2[1]
                    replacement_text = location_id
                    overwrite_text_in_file(text_to_search, replacement_text, dst)
                except:
                    print("Issue with {} in {} folder".format(store, folder))
                print("Updated folders for {}, adding {}".format(store, folder))
            else:
                src = blank_staging_folder + "\\" + folder + "\\" + "Kitchen.cfg"
                dst = network_drive_loc + store + "\\" + folder + "\\" + "Kitchen.cfg"
                r1 = network_drive_loc + store + "\\R1\\" + "Register.cfg"
                if os.path.isfile(dst):
                    os.remove(dst)
                shutil.copy(src, dst)
                filename = dst
                file = open(filename, "r")
                line = file.read()
                file.close()
                regex = re.search(r" (TerminalNumber=\"[1-9]*\")", line)
                replacement_text = get_kitchen_terminal_num(src)
                try:
                    text_to_search = regex[1]
                    overwrite_text_in_file(text_to_search, replacement_text, dst)
                except:
                    print("Issue with {}".format(store))

                filename = dst
                file = open(filename, "r")
                line = file.read()
                file.close()
                regex2 = r"(\w\w\w\w\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\-\w\w\w\w\w\w\w\w\w\w\w\w)"
                regexsearch2 = re.search(regex2, line)
                try:
                    text_to_search = regexsearch2[1]
                    replacement_text = location_id
                    overwrite_text_in_file(text_to_search, replacement_text, dst)
                except:
                    print("Issue with {} in {} folder".format(store, folder))
                print("Updated folders for {}, adding {}".format(store, folder))

            sleep(1)