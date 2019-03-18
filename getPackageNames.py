import os
from zipfile import ZipFile
from axmlparserpy import axmlprinter
from xml.dom import minidom
# import xml.etree.ElementTree as ET
import time
from subprocess import check_output

def get_manifest_content(apk):
    with ZipFile(apk, 'r') as zipObj:
       listOfFileNames = zipObj.namelist()
       for fileName in listOfFileNames:
           if fileName == 'AndroidManifest.xml':
               global flag
               try:
                   manifest = zipObj.read(fileName)
                   ap = axmlprinter.AXMLPrinter(manifest)
                   manifest_content = minidom.parseString(ap.getBuff()).toxml()
                   # with open ("AndroidManifestCopy.xml", "w") as f:
                   #     f.write(manifest_content)
                   flag = 1
                   return manifest_content
               except IndexError:
                   try:
                       #zipObj.extract(fileName)
                       aapt = check_output(["aapt.exe", "d", "badging", apk])
                       aapt_content = aapt.decode()
                       flag = 2
                       return aapt_content
                   except FileNotFoundError:
                       flag = 3
                       time.sleep(0.5)
                       # "Could not find aapt.exe"

def get_package_name(content):
    if flag == 1:
        # print(content) manifest_content
        name_start = content.find("package=") + len('package="')
        split = content[name_start:]
        name_end = split.find('"')
        name = split[:name_end]
        return name
    elif flag == 2:
        # print(content) aapt_content
        name_start = content.find("package") + len("package: name='")
        split = content[name_start:]
        name_end = split.find("'")
        name = split[:name_end]
        return name


with open("list.csv", "w") as outputfile:
    root = os.getcwd()

    for item in os.listdir(root):
        if os.path.isfile(os.path.join(root, item)):
            if ".apk" in item:
                nazwa_package = get_package_name(get_manifest_content(item))
                if flag == 3:
                    dozapisu = item + "," + "failed"+"\n"
                    outputfile.write(dozapisu)
                    print("!!! Could not find aapt.exe !!!")
                    time.sleep(0.5)
                    print(item + ": " + "failed")
                    time.sleep(0.5)
                else:
                    dozapisu = item + "," + nazwa_package+"\n"
                    outputfile.write(dozapisu)
                    print(item + ": " + nazwa_package)
                    time.sleep(0.5)

    print("\nlist.csv ready")
    os.system('pause')
