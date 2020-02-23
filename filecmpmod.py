from filecmp import dircmp

class dircmpfiles(dircmp):
    def report(self): # Print a report on the differences between a and b
        report = []
        # Output format is purposely lousy
        #print('diff', self.left, self.right)
        if self.left_only:
            self.left_only.sort()
            report.append('Only in {} : {}'.format(self.left, self.left_only))
        if self.right_only:
            self.right_only.sort()
            report.append('Only in {} : {}'.format(self.right, self.right_only))
        if self.same_files:
            self.same_files.sort()
            report.append('Identical files : {}'.format(self.same_files))
        if self.diff_files:
            self.diff_files.sort()
            report.append('Differing files : {}'.format(self.diff_files))
        if self.funny_files:
            self.funny_files.sort()
            report.append('Trouble with common files : {}'.format(self.funny_files))
        if self.common_dirs:
            self.common_dirs.sort()
            report.append('Common subdirectories : {}'.format(self.common_dirs))
        if self.common_funny:
            self.common_funny.sort()
            report.append('Common funny cases : {}'.format(self.common_funny))
        return report

    def report_partial_closure(self): # Print reports on self and on subdirs
        self.report()
        for sd in self.subdirs.values():
            print()
            sd.report()

    def report_full_closure(self,result): # Report on self and subdirs recursively
        result.append(self.report())
        print('\n\n -- (result)',result,'-- \n\n')
        for sd in self.subdirs.values():
            print()
            sd.report_full_closure()
        return result
# Specify the folders to compare 
REMOTE = r'D:\Ant Deployment\UAT-OMPL\sample\retrieveUnpackaged'
LOCAL = r'D:\Ant Deployment\MobileDev\sample\retrieveUnpackaged'

if __name__ == '__main__':
    dcmp = dircmpfiles(REMOTE, LOCAL)
    result = []
    print(dcmp.report_full_closure(result))
