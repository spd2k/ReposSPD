from Task import Task
import re

class Agregator():
	def __init__(self, filename):
		self.list_of_tasks = []
		self.numb_tasks = 0
		self.numb_machines = 0
		self.__read_data_from_file(filename)
		self.list_of_index = self.__fill_list_of_index(self.list_of_tasks)

	def __fill_list_of_index(self, list_of_tasks):
		list_of_index = []
		for i in list_of_tasks:
			list_of_index.append(i.nr)
		return list_of_index

	def __read_data_from_file(self, filename):
		with open(filename) as file:
			i = 0
			for f in file:
				dt = list(map(int, re.findall(r'\d+', f)))
				if i == 0:
					self.numb_tasks = dt[0]
					self.numb_machines = dt[1]
				else:
					self.list_of_tasks.append(Task(i - 1, dt))
				i += 1

	def __getCMax(self, numb_machines, list_of_index, list_of_tasks):
		MaxSpan = []
		for i in range(numb_machines):
			MaxSpan.append(0)
		for j in list_of_index:
			MaxSpan[0] += list_of_tasks[j].time[0]
			for k in range(1, numb_machines):
				if MaxSpan[k] < MaxSpan[k - 1]:
					MaxSpan[k] = MaxSpan[k - 1]
				MaxSpan[k] += list_of_tasks[j].time[k]
		return max(MaxSpan)

	def __permute(self, _list_of_tasks, low=0):
		if low + 1 >= len(_list_of_tasks):
			yield _list_of_tasks
		else:
			for p in self.__permute(_list_of_tasks, low + 1):
				yield p
			for i in range(low + 1, len(_list_of_tasks)):
				_list_of_tasks[low], _list_of_tasks[i] = _list_of_tasks[i], _list_of_tasks[low]
				for p in self.__permute(_list_of_tasks, low + 1):
					yield p
				_list_of_tasks[low], _list_of_tasks[i] = _list_of_tasks[i], _list_of_tasks[low]

	def find_best_order(self):
		min_cmax = self.__getCMax(self.numb_machines, self.list_of_index, self.list_of_tasks)
		best_order = []
		for i in self.__permute(self.list_of_index):
			permuted_tasks_Cmax = self.__getCMax(self.numb_machines, i, self.list_of_tasks)
			if permuted_tasks_Cmax < min_cmax:
				min_cmax = permuted_tasks_Cmax
				best_order = i
		return min_cmax, best_order

if __name__ == "__main__":
	foo = Agregator("test.txt")
	print(foo.find_best_order())
