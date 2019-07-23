import configparser
import ping3
import os, sys
import argparse
# import subprocess
import shutil
from tasks_models import *


config = configparser.ConfigParser()
arg_parser = None
args = None
single_tasks = []
mutiple_tasks = []

def load_tasks():
    global single_tasks
    config.read('tasks.ini')
    
    for task in config.sections():
        
        task_type = config[task]['task_type']

        if task_type == 'single':
        
            task_cmd = config[task]['task_cmd']

            if task_cmd == 'copy_folder':
                source = config[task]['source']
                dest = config[task]['dest']
                t = CopyTask(source, dest)
                t.task_type = config[task]['task_type']
                t.task_name = config[task]['task_name']
                t.task_cmd = config[task]['task_cmd']
                single_tasks.append(t)

            if task_cmd == 'copy_file':
                source = config[task]['source']
                dest = config[task]['dest']
                t = CopyTask(source, dest)
                t.task_type = config[task]['task_type']
                t.task_name = config[task]['task_name']
                t.task_cmd = config[task]['task_cmd']
                single_tasks.append(t)


def arguments():
    global args
    arg_parser = argparse.ArgumentParser(
        description='Automation tasks based on configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
        Usage example:

        tasky = tasky.py or tasky.exe
        tasky args

        -m --multiple          : Get a list of multiple tasks
        -s --single            : Get a list of single tasks
        -pa --perform_all      : Perform all multiple tasks
        -ps --perform_ind      : Perform all single tasks
        -po --perform_one      : Performs one single task
        -pm --perform_multiple : Performs one multiple task
        -pn --perform_number   : Performs task by number
        '''
    )

    arg_parser.add_argument('-m', '--multiple', dest='multiple', action='store_true', help='get multiple tasks')
    arg_parser.add_argument('-s', '--single', dest='single', action='store_true', help='get single tasks')
    arg_parser.set_defaults(multiple=False)
    arg_parser.set_defaults(single=False)
    args = arg_parser.parse_args()

def main():
    global args
    load_tasks()
    arguments()

    if args.multiple:
        print("Print multiple tasks")
    if args.single:
        print("Print single tasks")
        # index - task_cmd - task_name
        for task in single_tasks:
            if task.task_cmd == 'copy_folder':
                task.copy_folder()
        #     if task.task_cmd == 'copy_file':
        #         task.copy_file()
        # for index, task in enumerate(single_tasks):
        #     print(' - [%s] Task Name: %s Task Cmd: %s \n' % (index, task.task_name, task.task_cmd))
    
   

if __name__ == '__main__':
    main()