from filecmp import dircmp
import PySimpleGUI as sg

# Specify the folders to compare
# REMOTE = r'E:\Python Projects\Package Creator\remote'
# LOCAL = r'E:\Python Projects\Package Creator\local'


# method to print the diff
def get_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left,
                                                   dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)


if __name__ == '__main__':
    sg.theme('Light Blue 2')
    layout = [[sg.Text('Select the remote and the local folder')],
              [sg.Text('Remote', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
              [sg.Text('Local', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
              [sg.Submit(), sg.Cancel()]]
    window = sg.Window('Package Builder', layout)
    event, values = window.read()
    window.close()
    dcmp = dircmp(values[0], values[1])
    print_diff_files(dcmp)
