import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

import PySimpleGUI as sg

import script as sc

if __name__ == '__main__':
    package = ''
    sg.theme('Light Blue 2')
    layout = [[sg.Text('Select the remote and the local folder')],
              [sg.Text('Remote', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
              [sg.Text('Local', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
              [sg.Submit(), sg.Cancel()],
              [sg.Multiline(key='PacakgeOutput', size=(150, 20))],
              [sg.Button('Clear')]]
    window = sg.Window('Package Builder', layout, default_element_size=(120, 4))
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event in 'Submit':
            sc.REMOTE, sc.LOCAL = values[0], values[1]
            local_folders = next(os.walk(sc.LOCAL))[1]

            remote_folders = next(os.walk(sc.REMOTE))[1]

            # Find newly created folders and add their components to package.xml
            new_folders = set(local_folders) - set(remote_folders)
            # print(new_folders)
            for folder in new_folders:
                print(folder)
                sc.create_xml_elements_in_directory(sc.LOCAL, folder, sc.get_metadata(folder)['XMLName'])

            # For common folders
            common_folders = set(local_folders).intersection(set(remote_folders))
            # print(common_folders)
            for folder in common_folders:
                dcmp = sc.compare_directories(os.path.join(sc.REMOTE, folder), os.path.join(sc.LOCAL, folder))
                sc.create_members(dcmp.right_only, sc.get_metadata(folder)['XMLName'])
                sc.create_members(dcmp.diff_files, sc.get_metadata(folder)['XMLName'])
            dom = parseString(ET.tostring(sc.ROOT, encoding='unicode'))
            window['PacakgeOutput'].update(dom.toprettyxml())
        elif event in 'Clear':
            window['PacakgeOutput'].update('')

    window.close()