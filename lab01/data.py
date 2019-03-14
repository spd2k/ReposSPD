from Task import Task
import re

def read_data_from_file(filename):
    list_of_tasks = []
    with open(filename) as file:
        i = 0
        for f in file:
            dt = list(map(int, re.findall(r'\d+', f)))
            if i==0:
                numb_tasks = dt[0]
                numb_machines = dt[1]
            else:
                list_of_tasks.append(Task(i-1, dt))
            i += 1
    return list_of_tasks, numb_machines, numb_tasks

def fill_list_of_index(list_of_tasks):
    list_of_index = []
    for i in list_of_tasks:
        list_of_index.append(i.nr)
    return list_of_index





