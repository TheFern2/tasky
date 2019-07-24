import configparser
import ping3
import os, sys
import argparse
# import subprocess
import shutil
from tasks_models import *
import json
import datetime


config = configparser.ConfigParser()
arg_parser = None
args = None
single_tasks = []
mutiple_tasks = []
log = open('log.txt', 'a+')
now = datetime.datetime.now()

def load_single_tasks():
    global config
    global single_tasks

    for task in config.sections():
        
        task_type = config[task]['task_type']

        if task_type == 'single':
        
            task_cmd = config[task]['task_cmd']

            if task_cmd == 'copy_folder':
                #source = config[task]['source']
                source = json.loads(config.get(task, 'source'))
                #dest = config[task]['dest']
                dest = json.loads(config.get(task, 'dest'))
                t = CopyTask(source, dest)
                t.task_type = config[task]['task_type']
                t.task_name = config[task]['task_name']
                t.task_cmd = config[task]['task_cmd']
                single_tasks.append(t)

            if task_cmd == 'copy_file':
                source = json.loads(config.get(task, 'source'))
                dest = json.loads(config.get(task, 'dest'))
                t = CopyTask(source, dest)
                t.task_type = config[task]['task_type']
                t.task_name = config[task]['task_name']
                t.task_cmd = config[task]['task_cmd']
                single_tasks.append(t)

def load_multiple_tasks():
    global config
    global mutiple_tasks

    for task in config.sections():
        
        task_type = config[task]['task_type']

        if task_type == 'multiple':
            t = MultipleTask(task, task_type, single_tasks)
            mutiple_tasks.append(t)

def load_tasks():
    load_single_tasks()
    load_multiple_tasks()

def arguments():
    global args
    arg_parser = argparse.ArgumentParser(
        description='Automation tasks based on configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
        Usage example:

        tasky = tasky.py or tasky.exe
        tasky args*

        To perform one task by number:
        tasky -sn 1

        To perform one multiple task by number:
        tasky -mn 1

        '''
    )

    arg_parser.add_argument('-m', '--multiple', dest='multiple', action='store_true', help='multiple tasks')
    arg_parser.add_argument('-s', '--single', dest='single', action='store_true', help='single tasks')
    arg_parser.add_argument('-a', '--all', dest='all', action='store_true', help='all tasks')
    arg_parser.add_argument('-p', '--print', dest='print', action='store_true', help='prints')
    arg_parser.add_argument('-n', '--number', type=int)
    arg_parser.set_defaults(multiple=False)
    arg_parser.set_defaults(single=False)
    arg_parser.set_defaults(print=False)
    arg_parser.set_defaults(all=False)
    args = arg_parser.parse_args()


def perform_single_task_by_number(task_number):
    task = single_tasks[task_number]
    perform_single_task_by_cmd(task)


def perform_multiple_task_by_number(task_number):
    m_task = mutiple_tasks[task_number]
    tasks = m_task.tasks

    for task in tasks:
        perform_single_task_by_cmd(task)

def perform_single_task_by_name(task_name):
    pass

# Add more tasks here to avoid code repetition
def perform_single_task_by_cmd(task):
    if task.task_cmd == 'copy_folder':
        task.copy_folder()
    if task.task_cmd == 'copy_file':
        task.copy_file()

def main():
    global args
    global config
    config.read('tasks.ini')
    load_tasks()
    arguments()

    if args.multiple and args.print:
        print("Print multiple tasks")
        for index, task in enumerate(mutiple_tasks):
            print(' - [%s] Task Name: %s\n' % (index, task.section_name)) # maybe add number of tasks
    if args.single and args.print:
        print("Single tasks")
        for index, task in enumerate(single_tasks):
            print(' - [%s] Task Name: %s Task Cmd: %s \n' % (index, task.task_name, task.task_cmd))
    if args.single and args.number is not None:
        if args.number < len(single_tasks) and args.number >= 0:
            perform_single_task_by_number(args.number)
        else:
            print("Enter a task number with -n argument, without exceding single task list -s")
    if args.single and args.number is None and not args.print:
        print("-n argument is required with -t i.e -tn 2")
    if args.multiple and args.number is not None:
        if args.number < len(mutiple_tasks) and args.number >= 0:
            perform_multiple_task_by_number(args.number)
        else:
            print("Enter a task number with -n argument, without exceding single task list -s")
    if args.multiple and args.number is None and not args.print:
        print("-n argument is required with -m i.e -mn 2")
    if args.all and args.single:
        pass # do all single tasks
    if args.all and args.multiple:
        pass # do all multiple tasks

if __name__ == '__main__':
    main()