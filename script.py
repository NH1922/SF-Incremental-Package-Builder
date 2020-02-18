from filecmp import dircmp

# Specify the folders to compare 
REMOTE = r'E:\Python Projects\Package Creator\remote'
LOCAL = r'E:\Python Projects\Package Creator\local'


# method to print the diff 
def print_diff_files(dcmp,coms):
    for name in dcmp.diff_files:
        coms.append("diff_file %s found in %s and %s" % (name, dcmp.left,
                                                   dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)


if __name__=='__main__':
    dcmp = dircmp(REMOTE, LOCAL)
    coms = []
    print_diff_files(dcmp,coms)
    print(coms)