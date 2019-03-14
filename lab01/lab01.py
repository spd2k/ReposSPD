list_nr = []
list_times_m1 = []
list_times_m2 = []
with open('test.txt') as f:
    numb_tasks, numb_machines = [int(x) for x in next(f).split()] 
    array = []
    i=0
    for line in f: # read rest of lines
        a, b = [int(x) for x in line.split()]
        list_times_m1.append(a)
        list_times_m2.append(b)
for i in range(numb_tasks):
    list_nr.append(i)
print(numb_tasks)
print(numb_machines)
print(list_times_m1)
print(list_times_m2)
print(list_nr)

