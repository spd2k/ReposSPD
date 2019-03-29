from Task import Task
import re
import time

class Agregator():
	def __init__(self, filename):
		self.list_of_tasks = []
		self.numb_tasks = 0
		self.numb_machines = 0
		self.__read_data_from_file(filename)
		self.list_of_index = self.__fill_list_of_index(self.list_of_tasks)

	def __get_task_order(self, list_of_tasks):
		return [i.nr for i in list_of_tasks]

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

	def __getCMax(self, list_of_index, list_of_tasks):
		MaxSpan = []
		for i in range(self.numb_machines):
			MaxSpan.append(0)
		for j in list_of_index:
			MaxSpan[0] += list_of_tasks[j].time[0]
			for k in range(1, self.numb_machines):
				if MaxSpan[k] < MaxSpan[k - 1]:
					MaxSpan[k] = MaxSpan[k - 1]
				MaxSpan[k] += list_of_tasks[j].time[k]
		return max(MaxSpan)

	def Cmax_test(self):
		return self.__getCMax(self.list_of_index, self.list_of_tasks)

	def __permute(self, task_order, low=0):
		if low + 1 >= len(task_order):
			yield task_order
		else:
			for p in self.__permute(task_order, low + 1):
				yield p
			for i in range(low + 1, len(task_order)):
				task_order[low], task_order[i] = task_order[i], task_order[low]
				for p in self.__permute(task_order, low + 1):
					yield p
				task_order[low], task_order[i] = task_order[i], task_order[low]

	def johnson(self, list_of_tasks, numb_machines):
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
					# second_half.insert(0, list_of_tasks[min_m2])
					del list_of_tasks[min_m1]
				elif list_of_tasks[min_m1].time[0] > list_of_tasks[min_m2].time[1]:
					second_half.insert(0, list_of_tasks[min_m2].nr)
					del list_of_tasks[min_m2]
				if len(list_of_tasks) == 0:
					list_not_empty = False

		final_list = first_half + second_half
		return final_list

	def permute_for_best_order(self):
		min_cmax = self.__getCMax(self.list_of_index, self.list_of_tasks)
		best_order = []
		print(self.list_of_index)
		for permuted_order_of_tasks in self.__permute(self.list_of_index):
			permuted_tasks_Cmax = self.__getCMax(permuted_order_of_tasks, self.list_of_tasks)
			if permuted_tasks_Cmax < min_cmax:
				min_cmax = permuted_tasks_Cmax
				best_order = permuted_order_of_tasks
		return min_cmax, best_order

	def __NEH_best_order(self, current_list, new_task):
		task_list = []
		for place in range(len(current_list) + 1):
			updated_list = current_list[:]
			updated_list.insert(place, new_task)
			task_list.append(updated_list)
		cemax = lambda lista: self.__getCMax(list(range(len(lista))), lista)
		task_list.sort(key=cemax)
		return task_list[0]

	def NEH(self):
		# decreasingly sort
		priorities = lambda task: task.priority
		tasks_to_sort = self.list_of_tasks[:]
		tasks_to_sort.sort(reverse=True, key=priorities)
		biggest_Task = tasks_to_sort[0]
		NEH_list = [biggest_Task, ]
		for task in tasks_to_sort[1:]:
			NEH_list = self.__NEH_best_order(NEH_list, task)
		return self.__getCMax(list(range(len(NEH_list))), NEH_list), self.__get_task_order(NEH_list)

	def do_the_Johnson(self):
		return self.johnson(self.list_of_tasks, self.numb_machines)

if __name__ == "__main__":
	file = "ta001.txt"

	foo = Agregator(file)
	goo = Agregator(file)

#	permute_start = time.time()
#	print(foo.permute_for_best_order())
#	permute_end = time.time()
#	print(permute_end - permute_start)
	print("_________________________________")
	print("NEH: ")
	NEH_start = time.time()
	print(goo.NEH())
	NEH_end = time.time()
	print(NEH_end - NEH_start)

