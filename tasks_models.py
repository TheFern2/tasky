import shutil, os

# task types: copy, ping, open, compare, zip, del, ftp...

# Task Base Class
class Task(object):
    def __init__(self, section_name):
        self.section_name = ''
        self.task_type = ''
        self.task_name = ''
        self.task_cmd = ''


'''
CopyTask subclass of Task:

Class to instantiate tasks that require copying files or folders.
Source, and Dest can be multiple delimited by a comma at the input side
'''
class CopyTask(Task):
    def __init__(self, source, dest):
        self.source = []
        self.dest = []
        for path in source:
            self.source.append(path)
        for path in dest:
            self.dest.append(path)
    
    def copy_folder(self):
        for source in self.source:
            for dest in self.dest:
                copytree2(self.source, self.dest)
    
    def copy_file(self):
        for source in self.source:
            for dest in self.dest:
                shutil.copy(self.source, self.dest)


# Custom copytree2 in case folder is already created
# https://stackoverflow.com/a/12514470/1013828
def copytree2(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)