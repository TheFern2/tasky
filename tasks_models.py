import shutil, os
from tasky import log
from tasky import now

# task types: copy, ping, exec, compare, zip, del, ftp...

# MultipleTask
class MultipleTask(object):
    def __init__(self, section_name, task_type, tasks):
        self.section_name = section_name
        self.task_type = task_type
        self.tasks = tasks

# Task Base Class
class Task(object):
    def __init__(self, section_name):
        self.section_name = section_name
        self.task_type = ''
        self.task_name = ''
        self.task_cmd = ''


'''
CopyTask subclass of Task:

Class to instantiate tasks that require copying files or folders.
Source, and Dest can be multiple used as json with configparse in tandem
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
                try:
                    copytree2(source, dest)
                except Exception as e:
                    print("Did not find file") # this needs to be logged!
                    log.write("%s Copy Folder Error %s\n" % (now.strftime("%c"), e))
    
    def copy_file(self):
        for source in self.source:
            for dest in self.dest:
                try:
                    shutil.copy(source, dest)
                except Exception as e:
                    print("Did not find file") # this needs to be logged!
                    log.write("%s Copy File Error %s\n" % (now.strftime("%c"), e))


class ExecTask(Task):
    pass


class CompareTask(Task):
    pass


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