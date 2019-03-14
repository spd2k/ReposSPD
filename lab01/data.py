from Task import Task
import re

def read_data_from_file(filename):
    list_of_tasks = []
    with open(filename) as file:
        i = 0
        for line in file:
            dt = list(map(int, re.findall(r'\d+', line)))
            if i==0:
                numb_tasks = dt[0]
                numb_machines = dt[1]
            else:
                list_of_tasks.append(Task(i-1, dt))
            i += 1
    return list_of_tasks, numb_machines, numb_tasks

a,b,c = read_data_from_file("test.txt")
print(a[0].time[0])
print(a[0].time[1])




