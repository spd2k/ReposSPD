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
		self.global_UB = 0
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

	def __last_task_on_critic_track(self, pi_, C_max):
		offset =0
		for i in range(len(pi_)-1, 0, -1):
			inner_time=0
			q_time = pi_[i].time[2]
			for j in range(len(pi_)-1-offset, -1, -1):
				tmp=pi_[j].time[1]
				inner_time+=tmp
				r_time = pi_[j].time[0]
				computed_time = q_time + inner_time + r_time
				if computed_time == C_max:
					return i
			offset +=1
		else: return None

	def __first_task_on_critic_track(self, pi_, b_idx, Cmax):
		inner_time = 0
		q_time = pi_[b_idx].time[2]
		for i in range(b_idx, -1, -1):
			tmp=pi_[i].time[1]
			inner_time+=tmp
			r_time = pi_[i].time[0]
			computed_time = q_time + inner_time + r_time
			if computed_time == Cmax:
				return i
		else: return

	def critic_task(self, critic_list):
		min_task = critic_list[-1] # last q time task by default
		for task in range(len(critic_list)-1, -1, -1): # itering from last to first
			if critic_list[task].time[2] < min_task.time[2]: # check q times for each
				min_task = critic_list[task] # if any less
				return min_task
		else: return None

	def __count_time(self, tasks, sign):
		time = 2
		if sign == "r":
			time = 0
		elif sign == "p":
			time = 1
		else :
			time = 2
		counted_time = 0
		for job in tasks:
			counted_time += job.time[time]
		return counted_time

	def h(self, K, C=None):
		K_prim = K[:]
		if C is not None:
			K_prim.append(C)
		p_K_prim = self.__count_time(K_prim, "p")
		r_K_prim = min([i.time[0] for i in K_prim])
		q_K_prim = min([i.time[2] for i in K_prim])
		h_K = p_K_prim + r_K_prim + q_K_prim
		return h_K


	def Carlier(self, up_bound, list_of_tasks):
		U, pi = self.Schrage(list_of_tasks[:])
		pi_ = []
		UB = up_bound
		if U < UB :
			UB = U
			pi_ = pi[:]
		b_idx = self.__last_task_on_critic_track(pi, U)
		a_idx = self.__first_task_on_critic_track(pi[0:b_idx+1], b_idx, U)
		c = self.critic_task(pi[a_idx:b_idx+1])
		if c != None:

			c_idx = pi.index(c)
			K = pi[c_idx+1:b_idx+1]
			p_K = self.__count_time(K, "p")
			r_K = min([i.time[0] for i in K])
			q_K = min([i.time[2] for i in K])
			R_time_backup = c.time[0]
			c.time[0] = max([c.time[0], r_K + p_K])

			h_K = self.h(K)
			h_K_C = self.h(K, c)

			LB = self.SchragePmtn(pi)
			LB = max([h_K, h_K_C, LB])
			if LB < UB :
				pi = self.Carlier(UB, pi[:])

			c.time[0] = R_time_backup # back to the original pi
			Q_time_backup = c.time[2] #backup for qtime

			c.time[2] = max(c.time[2], q_K + p_K)
			LB = self.SchragePmtn(pi)
			h_K = self.h(K)
			h_K_C = self.h(K, c)
			LB = max([h_K, h_K_C, LB])
			if LB < UB :
				pi = self.Carlier(UB, pi[:])
			c.time[2] = Q_time_backup
			return pi
		else:
			self.global_UB= UB
			return pi


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

def check_schrage():
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

def check_Carlier():
	filenames = ["data0.txt","data1.txt","data2.txt","data3.txt","data4.txt","data5.txt","data6.txt","data7.txt","data8.txt",]#["in50.txt", "in100.txt", "in200.txt"]
	for file in filenames:
		print("-------------------------------------------------")
		foo = Agregator(file)
		result = foo.Carlier(900000000000, foo.list_of_tasks)
		print(file)
		# for i in result:
		# 	print(i.nr, end =" ")

		print('\n', foo.global_UB)

if __name__ == "__main__":
	check_Carlier()
	# foo = Agregator("makuch3.txt")
	# lista = foo.list_of_tasks
	# pi, u=foo.Carlier(900000000000, lista)
