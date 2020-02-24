from filecmp import dircmp

# Specify the folders to compare 
REMOTE = r'D:\Ant Deployment\UAT-OMPL\sample\retrieveUnpackaged'
LOCAL = r'D:\Ant Deployment\MobileDev\sample\retrieveUnpackaged'


# method to print the diff 
def print_diff_files(dcmp,coms):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left,
                                                   dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp,coms)


if __name__=='__main__':
    dcmp = dircmp(REMOTE, LOCAL)
    # coms = []
    # print_diff_files(dcmp,coms)
    # print(coms)
    # print ('--- Report---')
    # dcmp.report()
    # print('\n\n\n')
    print ('--- Report FuLL Closure---')
    dcmp.report_full_closure()
    # print('\n\n\n')
    # print ('--- Report partial Closure---')
    # print('\n\n\n')
    # dcmp.report_full_closure()
