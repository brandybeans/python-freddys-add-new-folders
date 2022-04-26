import fileinput
import os
import shutil
import re
from time import sleep

''' Blank Staging File folder location '''
blank_staging_folder = r"\\192.168.1.100\map_as_y\Brink\Customers\FFC\pdill\Blank Staging File - Brink"

''' NAS folder location '''
network_drive_loc = "\\\\192.168.1.100\\map_as_y\\Brink\\Customers\\FFC\\Staging\\"

folders = [
        'R6',
        'R7',
        'R8',
        'R9'
]

storefolders = os.listdir(network_drive_loc)
print(storefolders)
for store in storefolders:
    #print(network_drive_loc+store+"\\R1\\Register.cfg")
    if os.path.isfile(network_drive_loc+store+"\\R1\\Register.cfg"):
        #print(store)
        for folder in folders:
            if not os.path.isdir(network_drive_loc+store+"\\"+folder):

                os.makedirs(network_drive_loc+store+"\\"+folder)
                src = network_drive_loc+store+ "\\R1\\Register.cfg"
                dst = network_drive_loc+store+ "\\" + folder + "\\" + "Register.cfg"
                shutil.copy(src, dst)
                filename = dst
                file = open(filename, "r")
                line = file.read()
                file.close()
                regex = re.search(r" (TerminalNumber=\"[1-9]\")", line)
                replacement_text = "TerminalNumber=\"" + folder[1] + "\""
                try:
                    text_to_search = regex[1]
                except:
                    print("Issue with {}".format(store))
                with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
                    for line in file:
                        print(line.replace(text_to_search, replacement_text), end='')
                print("Updated folders for {}, adding {}".format(store, folder))
                sleep(1)