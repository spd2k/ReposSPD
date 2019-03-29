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

#Sprawozdanie
'''
Ponieważ przy poszukiwaniu za pomocą permutacji kolejnosci zadań przy dużej ich ilości zadań pamięć komputera szybko sięzapełniała.
Algorytm NEH dla instacji ta001 dawał wynik:
NEH: 
(1286, [2, 16, 8, 7, 14, 13, 10, 15, 12, 18, 5, 3, 4, 17, 0, 1, 9, 6, 19, 11])
TIME: 0.030000686645507812

dla instacji ta120 czas był równy = 751.6 sekundczyli  ponad 11 minut. Wynik taki sam jak w przykladzie z danych.
NEH: 
(26984, [15, 225, 133, 43, 308, 11, 315, 136, 271, 244, 338, 405, 229, 261, 170, 149, 484, 108, 411, 105, 376, 395, 46, 245, 224, 286, 157, 446, 282, 485, 375, 359, 345, 452, 186, 305, 218, 435, 273, 110, 374, 243, 154, 249, 200, 113, 276, 414, 248, 147, 388, 167, 385, 365, 362, 55, 255, 42, 129, 24, 84, 3, 188, 409, 135, 486, 380, 331, 250, 310, 12, 389, 121, 277, 95, 377, 438, 203, 151, 393, 47, 44, 10, 126, 303, 481, 265, 364, 320, 28, 454, 73, 54, 220, 387, 307, 130, 115, 312, 30, 322, 169, 319, 437, 5, 141, 415, 433, 112, 464, 226, 445, 406, 237, 191, 187, 65, 379, 180, 212, 373, 193, 332, 232, 316, 453, 32, 174, 394, 210, 38, 287, 213, 124, 53, 290, 90, 422, 134, 190, 0, 21, 269, 219, 378, 214, 496, 171, 404, 80, 450, 27, 67, 391, 18, 127, 246, 398, 175, 296, 451, 9, 333, 142, 334, 313, 494, 66, 403, 421, 489, 295, 278, 4, 289, 34, 176, 469, 251, 236, 407, 222, 324, 216, 1, 74, 420, 473, 58, 241, 165, 465, 45, 201, 340, 128, 89, 41, 196, 140, 62, 107, 217, 293, 75, 372, 7, 91, 182, 152, 37, 148, 206, 462, 336, 270, 301, 51, 197, 76, 252, 361, 59, 284, 381, 330, 275, 194, 424, 164, 363, 272, 327, 339, 150, 457, 400, 488, 497, 288, 153, 35, 56, 29, 168, 300, 298, 482, 498, 235, 146, 397, 352, 425, 48, 474, 204, 264, 426, 370, 483, 408, 20, 390, 199, 36, 64, 88, 399, 460, 434, 297, 346, 448, 192, 268, 87, 137, 97, 357, 231, 63, 118, 184, 480, 19, 353, 233, 444, 342, 96, 69, 161, 173, 280, 162, 427, 384, 358, 306, 382, 160, 468, 6, 242, 493, 294, 215, 318, 470, 447, 274, 449, 443, 266, 131, 234, 26, 116, 22, 81, 103, 431, 109, 119, 429, 285, 442, 317, 79, 323, 279, 335, 329, 499, 253, 82, 16, 479, 17, 156, 172, 132, 122, 100, 155, 57, 328, 92, 383, 299, 402, 344, 195, 366, 477, 179, 292, 101, 343, 208, 159, 492, 354, 490, 123, 178, 77, 163, 144, 417, 230, 198, 125, 281, 355, 223, 78, 348, 8, 202, 302, 94, 227, 93, 491, 98, 456, 349, 466, 158, 392, 177, 347, 40, 99, 71, 371, 139, 33, 52, 259, 441, 117, 267, 418, 423, 221, 258, 487, 60, 257, 50, 238, 416, 360, 39, 455, 138, 209, 495, 86, 304, 367, 471, 143, 262, 72, 321, 205, 368, 189, 85, 463, 254, 283, 102, 419, 311, 239, 467, 428, 439, 31, 401, 2, 314, 183, 351, 247, 256, 410, 461, 120, 68, 263, 472, 13, 291, 211, 476, 185, 396, 458, 70, 356, 325, 166, 475, 309, 23, 436, 430, 260, 413, 111, 61, 337, 181, 326, 440, 341, 49, 114, 412, 350, 106, 145, 369, 104, 432, 478, 83, 207, 25, 228, 14, 240, 459, 386])
TIME : 751.6154239177704

Wyniki natomiast pokrywały się jedynie tablica kolejności przybrała inną forme tylko ze względu na indexowanie ktore w w naszym programie jest od 0 a w podanych wynikach od 1..
Wnioski:
Oczywistym jest także że algorytm NEH działał zdecydowanie szybciej ze względu na dużo mniejszą liczbę porównań ponieważ ilość przy permutowaniu 
wynosić będzie ilość maszyn silnia
Natomiast przy NEHu możliwych opcji jest: [1+2+...n] Więc ilość nie rośnie jak funkcja silni jednak proporcjonalnie. Ilość operacji jest znacznie znacznie mniejsza, 
'''