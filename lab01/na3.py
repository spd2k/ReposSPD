from data import read_data_from_file
from data import fill_list_of_index

def cmax(numb_machines, list_of_index, list_of_tasks):
    endtime = []
    for i in range(numb_machines):
        endtime.append(0)
    for j in list_of_index:
        endtime[0] += list_of_tasks[j].time[0]
        for k in range(1, numb_machines):
            if endtime[k] < endtime[k-1]:
                endtime[k] = endtime[k-1]
            endtime[k] += list_of_tasks[j].time[k]
    return max(endtime)

def permute(xs, low=0):
    if low + 1 >= len(xs):
        yield xs
    else:
        for p in permute(xs, low + 1):
            yield p
        for i in range(low + 1, len(xs)):
            xs[low], xs[i] = xs[i], xs[low]
            for p in permute(xs, low + 1):
                yield p
            xs[low], xs[i] = xs[i], xs[low]

