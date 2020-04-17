import json
import os
from lxml import etree
from filecmp import dircmp
from xml.dom import minidom

# Specify the folders to compare
REMOTE = 'D:/Salesforce Workspace/Ant Deployment/salesforce_ant_48.0/sample/retrieveUnpackagedUAT'
LOCAL = 'D:/Salesforce Workspace/Ant Deployment/salesforce_ant_48.0/sample/retrieveUnpackaged'
METADATA = json.load(open('metadata.json'))



# Search in metadata
def get_metadata(name):
    for data in METADATA:
        if(data['DirName'] == name):
            return data


# Perform XML related initialization
# ET.register_namespace('', "http://soap.sforce.com/2006/04/metadata")
NAMESPACE = "http://soap.sforce.com/2006/04/metadata"
NSMAP = {None:NAMESPACE}
ROOT = etree.Element('Package',nsmap=NSMAP)



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
    if len(members) > 0:
        types = etree.SubElement(ROOT, 'types')
        for member in members:
            element = etree.SubElement(types, 'members')
            element.text = member.split('.')[0]
        name = etree.SubElement(types, 'name')
        name.text = metadata_type


def write_xml():
    etree.indent(ROOT,space='\t')
    et = etree.ElementTree(ROOT)
    #et.write('Package.xml',xml_declaration=True,encoding='UTF-8',standalone=True)
    return etree.tostring(ROOT,xml_declaration=True,encoding='UTF-8',standalone=True)
    #return etree.tostring(ROOT,xml_declaration=True,encoding='unicode',standalone=True)
    # rint(etree.tostring(ROOT,pretty_print=True,xml_declaration=True,encoding='UTF-8',standalone=True))
    #tree = ET.ElementTree(ROOT)
    #tree.write('op.xml',encoding='UTF-8',xml_declaration=True,default_namespace='http://soap.sforce.com/2006/04/metadata',method='xml')
    #xmlstr = minidom.parseString(ET.tostring(
    #    ROOT, encoding='UTF-8')).toprettyxml(indent="   ")
    #with open("Test.xml", "w") as f:
    #    f.write(xmlstr)


if __name__ == '__main__':
    local_folders = next(os.walk(LOCAL))[1]

    remote_folders = next(os.walk(REMOTE))[1]

    # Find newly created folders and add their components to package.xml
    new_folders = set(local_folders) - set(remote_folders)
    # print(new_folders)
    for folder in new_folders:
        print(folder)
        create_xml_elements_in_directory(LOCAL,folder,get_metadata(folder)['XMLName'])

    # For common folders
    common_folders = set(local_folders).intersection(set(remote_folders))
    # print(common_folders)
    for folder in common_folders:
        dcmp = compare_directories(os.path.join(REMOTE,folder),os.path.join(LOCAL,folder))
        create_members(dcmp.right_only,get_metadata(folder)['XMLName'])
        create_members(dcmp.diff_files,get_metadata(folder)['XMLName'])
    write_xml()
