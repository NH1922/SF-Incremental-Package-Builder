import json
import os
import xml.etree.ElementTree as ET
from filecmp import dircmp
from xml.dom import minidom

# Specify the folders to compare
REMOTE = r'D:\Projects\SF-Incremental-Package-Builder\remote\unpackaged'
LOCAL = r'D:\Projects\SF-Incremental-Package-Builder\local\unpackaged'
METADATA = json.load(open('metadata.json'))



# Search in metadata
def get_metadata(name):
    for data in METADATA:
        if(data['DirName'] == name):
            return data


# Perform XML related initialization
ET.register_namespace('', "http://soap.sforce.com/2006/04/metadata")
ROOT = ET.Element('Package')


def compare_directories(REMOTE, LOCAL):
    dcmp = dircmp(REMOTE, LOCAL)
    return dcmp


def create_xml_elements_in_directory(local,directory,metadata_type):
    # Fetch all the files in the directory
    folder_content = []
    members = []
    current_directory = os.path.join(local, directory)
    all_folders = next(os.walk(current_directory))[1]
    files = next(os.walk(current_directory))[2]
    if(files):
        members = [file.split('.')[0] for file in files]
    # print('Files within folder {} are {} '.format(directory,members))
    # print('Folders within folder {} are {} '.format(directory,all_folders))
    
    if all_folders:
        if not get_metadata(directory)['InFolder']:
            members = all_folders
        else:
            for folder in all_folders:
                folder_content.append({folder:next(os.walk(os.path.join(current_directory,folder)))[2]})

    if(folder_content):
        for folder in folder_content:
            for key,value in folder.items():
                for file in value:
                    members.append('{}/{}'.format(key,file.split('.')[0]))
    # print(members)

    if members:
        create_members(members,metadata_type)

    # if directory == 'aura':
    #     create_members(members,'AuraDefinitionBundle')
    #     ET.dump(ROOT)

# Function to add members to types


def create_members(members, metadata_type):
    types = ET.SubElement(ROOT, 'types')
    for member in members:
        element = ET.SubElement(types, 'members')
        element.text = member
    name = ET.SubElement(types, 'name')
    name.text = metadata_type


def write_xml():
    xmlstr = minidom.parseString(ET.tostring(
        ROOT, encoding='UTF-8')).toprettyxml(indent="   ")
    with open("Test.xml", "w") as f:
        f.write(xmlstr)


if __name__ == '__main__':
    local_folders = next(os.walk(LOCAL))[1]

    remote_folders = next(os.walk(REMOTE))[1]

    # Find newly created folders and add their components to package.xml
    new_folders = set(local_folders) - set(remote_folders)
    # print(new_folders)
    for folder in new_folders:
        print(folder)
        create_xml_elements_in_directory(LOCAL,folder,get_metadata(folder)['DirName'])

    # For common folders
    common_folders = set(local_folders).intersection(set(remote_folders))
    # print(common_folders)
    for folder in common_folders:
        dcmp = compare_directories(os.path.join(REMOTE,folder),os.path.join(LOCAL,folder))
        create_members(dcmp.right_only,folder)
        create_members(dcmp.diff_files,folder)
    write_xml()
