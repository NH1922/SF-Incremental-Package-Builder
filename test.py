from filecmp import dircmp
from MetaParser import parse_meta
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom


# Specify the folders to compare 
REMOTE = r'D:\Ant Deployment\UAT-OMPL\sample\retrieveUnpackaged'
LOCAL = r'D:\Ant Deployment\MobileDev\sample\retrieveUnpackaged'
METADATA = parse_meta()

#Perform XML related initialization
ET.register_namespace('',"http://soap.sforce.com/2006/04/metadata")
ROOT = ET.Element('Package')


def compare_directories(REMOTE,LOCAL):
    dcmp = dircmp(REMOTE, LOCAL)
    return dcmp

def create_xml_elements_in_directory(directory):
    # Fetch all the files in the directory 
    members = os.listdir(os.path.join(LOCAL,directory))
    create_members(members,METADATA[directory])

    # if directory == 'aura':
    #     create_members(members,'AuraDefinitionBundle')
    #     ET.dump(ROOT)

# Function to add members to types
def create_members(members,metadata_type):
    types = ET.SubElement(ROOT,'types')
    for member in members:
        element = ET.SubElement(types,'members')
        element.text = member
    name = ET.SubElement(types,'name')
    name.text = metadata_type

#Function to write to xml 
def write_xml():
    xmlstr = minidom.parseString(ET.tostring(ROOT,encoding='UTF-8')).toprettyxml(indent="   ")
    with open("Test.xml", "w") as f:
        f.write(xmlstr)

if __name__=='__main__':
    diffs = []
    additional_folders = []
    dcmp = compare_directories(REMOTE, LOCAL)

    #Check for newly created elements

    if dcmp.left_list != dcmp.right_list:
        additional_folders = list(set(dcmp.right_list) - set(dcmp.left_list) )
    for folder in additional_folders:
        create_xml_elements_in_directory(folder)

    
    # tree = ET.ElementTree(ROOT)
    # tree.write('test.xml',encoding="UTF-8", xml_declaration=True)
   
    