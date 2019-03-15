from data import read_data_from_file
from na3 import cmax

def johnson(list_of_tasks, numb_machines):
    first_half = []
    second_half = []
    if numb_machines == 2:
        list_not_empty = True
        while list_not_empty:
            min_m1 = 0
            min_m2 = 0
            for task_nr in range(len(list_of_tasks)):
                if list_of_tasks[task_nr].time[0] < list_of_tasks[min_m1].time[0]:
                    min_m1 = task_nr
                if list_of_tasks[task_nr].time[1] < list_of_tasks[min_m2].time[1]:
                    min_m2 = task_nr
            if list_of_tasks[min_m1].time[0] < list_of_tasks[min_m2].time[1]:
                first_half.append(list_of_tasks[min_m1].nr)
                del list_of_tasks[min_m1]
            elif list_of_tasks[min_m1].time[0] == list_of_tasks[min_m2].time[1]:
                first_half.append(list_of_tasks[min_m1].nr)
                #second_half.insert(0, list_of_tasks[min_m2])
                del list_of_tasks[min_m1]
            elif list_of_tasks[min_m1].time[0] > list_of_tasks[min_m2].time[1]:
                second_half.insert(0, list_of_tasks[min_m2].nr)
                del list_of_tasks[min_m2]
            if len(list_of_tasks)==0:
                list_not_empty = False

    final_list = first_half + second_half
    return final_list

list_of_tasks, numb_machines, numb_tasks = read_data_from_file("test.txt");
a=johnson(list_of_tasks, numb_machines)
print("Order for Johnson's algorithm:")
print(a)

list_of_tasks, numb_machines, numb_tasks = read_data_from_file("test.txt")
b = cmax(numb_machines, a, list_of_tasks)
print("Makespan for Johnson's algorithm:")
print(b)

