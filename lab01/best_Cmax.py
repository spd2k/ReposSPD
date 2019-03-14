from data import fill_list_of_index
from data import read_data_from_file
from na3 import permute
from na3 import cmax

def best_cmax(numb_machines, list_of_tasks):
    list_of_index = fill_list_of_index(list_of_tasks)
    min_cmax = cmax(numb_machines, list_of_index, list_of_tasks)
    for i in permute(fill_list_of_index(list_of_tasks)):
        print("task order: ")
        print(i)
        print("Cmax: ")
        print(cmax(numb_machines, i, list_of_tasks))
        if cmax(numb_machines, i, list_of_tasks)<min_cmax:
            min_cmax = cmax(numb_machines, i, list_of_tasks)
    return min_cmax

list_of_tasks, numb_machines, numb_tasks = read_data_from_file("test.txt");
ind = fill_list_of_index(list_of_tasks)
a = best_cmax(numb_machines, list_of_tasks)
print("Minimum makespan: ")
print(a)