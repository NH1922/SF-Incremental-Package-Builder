from filecmp import dircmp
import PySimpleGUI as sg
import script as sc

# Specify the folders to compare
# REMOTE = r'E:\Python Projects\Package Creator\remote'
# LOCAL = r'E:\Python Projects\Package Creator\local'


# method to print the diff
def print_diff_files(dcmp,coms):
    for name in dcmp.diff_files:
        coms.append("diff_file %s found in %s and %s" % (name, dcmp.left,
                                                   dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)


if __name__ == '__main__':
    package = ''
    sg.theme('Light Blue 2')
    layout = [[sg.Text('Select the remote and the local folder')],
              [sg.Text('Remote', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
              [sg.Text('Local', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
              [sg.Submit(), sg.Cancel()],
               [sg.Multiline(key='PacakgeOutput', size=(65,5))]]
    window = sg.Window('Package Builder', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event in 'Submit':
            sc.REMOTE,sc.LOCAL = values[0],values[1]
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
            window['PacakgeOutput'].update('This is green text')
    window.close()
        #dcmp = dircmp(values[0], values[1])
        #coms = []
        #print_diff_files(dcmp.coms)
       #print(coms)
