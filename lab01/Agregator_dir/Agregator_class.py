from __future__ import print_function
from math import  exp
import random
from os import listdir
import os
path = '.'
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
		copy=list_of_tasks[:]
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
		cmax = self.__getCMax(final_list, copy)
		return cmax


	def permute_for_best_order(self):
		min_cmax = self.__getCMax(self.list_of_index, self.list_of_tasks)
		best_order = []
		print(self.list_of_index)
		for permuted_order_of_tasks in self.__permute(self.list_of_index):
			permuted_tasks_Cmax = self.__getCMax(permuted_order_of_tasks, self.list_of_tasks)
			if permuted_tasks_Cmax < min_cmax:
				min_cmax = permuted_tasks_Cmax
				best_order = permuted_order_of_tasks
		return min_cmax

	def __NEH_best_order(self, current_list, new_task):
		task_list = []
		for place in range(len(current_list) + 1):
			updated_list = current_list[:]
			updated_list.insert(place, new_task)
			task_list.append(updated_list)
		cemax = lambda lista: self.__getCMax(list(range(len(lista))), lista)
		task_list.sort(key=cemax)
		return task_list[0]

	def NEH(self,order=False):
		# decreasingly sort
		priorities = lambda task: task.priority
		tasks_to_sort = self.list_of_tasks[:]
		tasks_to_sort.sort(reverse=True, key=priorities)
		biggest_Task = tasks_to_sort[0]
		NEH_list = [biggest_Task, ]
		for task in tasks_to_sort[1:]:
			NEH_list = self.__NEH_best_order(NEH_list, task)
		if order:
			return self.__getCMax(list(range(len(NEH_list))), NEH_list)#, self.__get_task_order(NEH_list)
		else:
			return NEH_list

	def do_the_Johnson(self):
		return self.johnson(self.list_of_tasks, self.numb_machines)

	def __get_propability(self,pi, pi_prim, T):
		cprim = self.__getCMax(self.__fill_list_of_index(pi_prim), pi_prim)
		c = self.__getCMax(self.__fill_list_of_index(pi), pi)
		if cprim<c:
			return 1
		else:
			return exp((c-cprim)/T)

	def __get_random_tasks(self):
		first_random_task = random.randint(0, self.numb_tasks-1)
		second_random_task = random.randint(0, self.numb_tasks-1)
		while first_random_task == second_random_task:
			second_random_task = random.randint(0, self.numb_tasks-1)
		return first_random_task, second_random_task

	def SA(self, start_point,  Temperature, order = False, mode = 'insert'):
		q=0.8
		pi = start_point[:]
		while Temperature > 1000:
			pi_prim = pi
			if mode == 'insert':
				random_item = random.randint(0, self.numb_tasks-1)
				elem = pi_prim[random_item]
				del pi_prim[random_item]
				random_item = random.randint(0, self.numb_tasks-1)
				pi_prim.insert(random_item, elem)
			elif mode == 'swap':
				first_random_task, second_random_task = self.__get_random_tasks()
				pi_prim[first_random_task], pi_prim[second_random_task] = pi_prim[second_random_task], pi_prim[first_random_task]
			if self.__get_propability(pi, pi_prim, Temperature) > random.uniform(0,1):
				pi=pi_prim
			Temperature = (q*Temperature)
		if order:
			#return self.__getCMax(list(range(len(pi))), pi)#, self.__get_task_order(pi)
			return self.__getCMax(self.__fill_list_of_index(pi), pi)  # , self.__get_task_order(pi)
		else:
			print(Temperature)
			return pi

	def Schrage(self, list_tasks):
		Cmax=0
		G=[]
		pi=[]
		rj = lambda task: task.time[0]
		N = list_tasks[:]
		N.sort(reverse=False, key=rj)
		t=N[0].time[0]
		while(G or N):
			while(N and N[0].time[0]<=t):
				e=N[0]
				G.append(e)
				del N[0]
			if (not G):
				t=N[0].time[0]
			else:
				qj = lambda task: task.time[2]
				G.sort(reverse=True, key=qj)
				e=G[0]
				del G[0]
				pi.append(e)
				t=t+e.time[1]
				Cmax=max(Cmax, t+e.time[2])
		return Cmax, pi

	def SchragePmtn(self, list_tasks):
		Cmax = 0
		G = []
		N=list_tasks[:]
		rj = lambda task: task.time[0]
		N.sort(reverse=False, key=rj)
		t=0
		l=Task(0, [0,0,99999])
		while (G or N):
			while(N and N[0].time[0]<=t):
				e = N[0]
				G.append(e)
				del N[0]
				if (e.time[2] > l.time[2]):
					l.time[1] = t - e.time[0]
					t = e.time[0]
					if l.time[1] > 0:
						G.append(l)
			if not G:
				t=N[0].time[0]
			else:
				qj = lambda task: task.time[2]
				G.sort(reverse=True, key=qj)
				e = G[0]
				del G[0]
				l=e
				t=t+e.time[1]
				Cmax=max(Cmax, t+e.time[2])
		return Cmax






















def compare_Johnson_to_NEH():

	files = os.listdir(path)
	print(files)
	print("Johnson: ")
	files = ['1.txt', '10.txt', '11.txt', '12.txt', '13.txt', '14.txt', '15.txt', '16.txt', '17.txt', '18.txt', '19.txt', '2.txt', '3.txt', '4.txt', '5.txt', '6.txt', '7.txt', '8.txt', '9.txt']

	for plik in files[6:]:
		foo = Agregator(plik)
		print(str(foo.do_the_Johnson())+ "|", end="")
	print("")
	print("-------------------------------------------")

	print("NEH:")
	for plik in files[6:]:
		goo = Agregator(plik)
		print(str(goo.NEH()) + "|" , end="")
	print("")
	print("-------------------------------------------")
def compare_SA_to_NEH():

	files = os.listdir(path)
	temp=25000
	print(files)
	print("SA: ")
	files = ['1.txt', '10.txt', '11.txt', '12.txt', '13.txt', '14.txt', '15.txt', '16.txt', '17.txt', '18.txt', '19.txt', '2.txt', '3.txt', '4.txt', '5.txt', '6.txt', '7.txt', '8.txt', '9.txt']
	SA_start=time.time()
	for plik in files[6:]:
		foo = Agregator(plik)
		print(str(foo.SA(foo.list_of_tasks,temp,order=True))+ "|", end="")
	print("")
	print("-------------------------------------------")
	SA_stop=time.time()
	print(SA_stop-SA_start)
	NEH_start=time.time()
	print("NEH:")
	for plik in files[6:]:
		goo = Agregator(plik)
		print(str(goo.NEH(order=True)) + "|" , end="")
	print("")
	print("-------------------------------------------")
	NEH_stop=time.time()
	print(NEH_stop-NEH_start)



if __name__ == "__main__":
	print("Schrage")
	filename = "in50.txt"
	foo = Agregator(filename)
	print(foo.Schrage(foo.list_of_tasks))
	filename = "in100.txt"
	goo = Agregator(filename)
	print(goo.Schrage(goo.list_of_tasks))
	filename = "in200.txt"
	hoo = Agregator(filename)
	print(hoo.Schrage(hoo.list_of_tasks))
	print("SchragePMTN")
	filename = "in50.txt"
	foo = Agregator(filename)
	print(foo.SchragePmtn(foo.list_of_tasks))
	filename = "in100.txt"
	goo = Agregator(filename)
	print(goo.SchragePmtn(goo.list_of_tasks))
	filename = "in200.txt"
	hoo = Agregator(filename)
	print(hoo.SchragePmtn(hoo.list_of_tasks))


