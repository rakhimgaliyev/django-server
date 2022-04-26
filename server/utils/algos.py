import json
import copy
from haversine import haversine


def _dist(a, b):
	a = (a[0], a[1])
	b = (b[0], b[1])
	# print(haversine(a, b))
	return haversine(a, b)


def _data_distribution(array, cluster):
	k = len(cluster)
	n = len(array)
	dim = 2

	cluster_content = [[] for i in range(k)]

	for i in range(n):
		min_distance = float('inf')
		situable_cluster = -1
		for j in range(k):
			# distance = _dist(array[i], cluster[j])
			distance = 0
			for q in range(dim):
				distance += (array[i][q] - cluster[j][q]) ** 2

			distance = distance ** (1 / 2)
			if distance < min_distance:
				min_distance = distance
				situable_cluster = j

		cluster_content[situable_cluster].append(array[i])

	return cluster_content


def cluster_update(cluster, cluster_content, dim):
	k = len(cluster)
	for i in range(k): #по i кластерам
		for q in range(dim): #по q параметрам
			updated_parameter = 0
			for j in range(len(cluster_content[i])):
				updated_parameter += cluster_content[i][j][q]
			if len(cluster_content[i]) != 0:
				updated_parameter = updated_parameter / len(cluster_content[i])
			cluster[i][q] = updated_parameter
	return cluster


def clusterization(array, k):
	n = len(array)
	dim = len(array[0])

	cluster = [[0 for i in range(dim)] for q in range(k)]
	cluster_content = [[] for i in range(k)]

	# for i in range(dim):
	# 	for q in range(k):
	# 		# a = array[0][0]
	# 		# b = array[0][1]
	# 		# print(a, b)
	# 		# if a > b:
	# 		# 	a, b = b, a
	# 		cluster[q][i] = random.randint()
	for q in range(k):
		cluster[q] = array[q]

	cluster_content = _data_distribution(array, cluster)

	privious_cluster = copy.deepcopy(cluster)
	while 1:
		cluster = cluster_update(cluster, cluster_content, dim)
		cluster_content = _data_distribution(array, cluster)
		if cluster == privious_cluster:
			break
		privious_cluster = copy.deepcopy(cluster)

	return cluster_content


#Функция нахождения минимального элемента, исключая текущий элемент
def Min(lst, myindex):
    return min(x for idx, x in enumerate(lst) if idx != myindex)


#функция удаления нужной строки и столбцах
def _Delete(matrix, index1, index2):
    del matrix[index1]
    for i in matrix:
        del i[index2]
    return matrix


def _Komi(matrix):
	n = len(matrix)
	# matrix = []
	H = 0
	PathLenght = 0
	Str = []
	Stb = []
	res = []
	result = []
	StartMatrix = []

	# Инициализируем массивы для сохранения индексов
	for i in range(n):
		Str.append(i)
		Stb.append(i)

	# Вводим матрицу
	# for i in range(n): matrix.append(list(map(int, input().split())))

	# Сохраняем изначальную матрицу
	for i in range(n): StartMatrix.append(matrix[i].copy())

	# Присваеваем главной диагонали float(inf)
	for i in range(n): matrix[i][i] = float('inf')

	while True:
		# Редуцируем
		# --------------------------------------
		# Вычитаем минимальный элемент в строках
		for i in range(len(matrix)):
			temp = min(matrix[i])
			H += temp
			for j in range(len(matrix)):
				matrix[i][j] -= temp

		# Вычитаем минимальный элемент в столбцах
		for i in range(len(matrix)):
			temp = min(row[i] for row in matrix)
			H += temp
			for j in range(len(matrix)):
				matrix[j][i] -= temp
		# --------------------------------------

		# Оцениваем нулевые клетки и ищем нулевую клетку с максимальной оценкой
		# --------------------------------------
		NullMax = 0
		index1 = 0
		index2 = 0
		tmp = 0
		for i in range(len(matrix)):
			for j in range(len(matrix)):
				if matrix[i][j] == 0:
					tmp = Min(matrix[i], j) + Min((row[j] for row in matrix), i)
					if tmp >= NullMax:
						NullMax = tmp
						index1 = i
						index2 = j
		# --------------------------------------

		# Находим нужный нам путь, записываем его в res и удаляем все ненужное
		res.append(Str[index1] + 1)
		res.append(Stb[index2] + 1)

		oldIndex1 = Str[index1]
		oldIndex2 = Stb[index2]
		if oldIndex2 in Str and oldIndex1 in Stb:
			NewIndex1 = Str.index(oldIndex2)
			NewIndex2 = Stb.index(oldIndex1)
			matrix[NewIndex1][NewIndex2] = float('inf')
		del Str[index1]
		del Stb[index2]
		matrix = _Delete(matrix, index1, index2)
		if len(matrix) == 1: break

	# Формируем порядок пути
	# print("res", len(res))
	# print(res)
	for i in range(0, len(res) - 1, 2):
		if res.count(res[i]) < 2:
			result.append(res[i])
			result.append(res[i + 1])
	for i in range(0, len(res) - 1, 2):
		for j in range(0, len(res) - 1, 2):
			if result[len(result) - 1] == res[j]:
				result.append(res[j])
				result.append(res[j + 1])
	# print("----------------------------------")
	# print(result)

	# Считаем длину пути
	for i in range(0, len(result) - 1, 2):
		if i == len(result) - 2:
			PathLenght += StartMatrix[result[i] - 1][result[i + 1] - 1]
			PathLenght += StartMatrix[result[i + 1] - 1][result[0] - 1]
		else:
			PathLenght += StartMatrix[result[i] - 1][result[i + 1] - 1]
	# print(PathLenght)
	# print("----------------------------------")
	return result


def algos(templates):
	start = templates[0]
	st_x = start['position']['x']
	st_y = start['position']['y']
	st = [st_x, st_y]
	templates = templates[1:]

	# print(len(templates))
	m = dict()
	a = []
	X = []
	Y = []
	for i in templates:
		x = i['position']['x']
		y = i['position']['y']
		X.append(x)
		Y.append(y)
		m[(x, y)] = i['id']
		a.append([x, y])

	# количество кластеров
	kol_kl = 2
	res = clusterization(a, kol_kl)

	result = [[] for i in range(kol_kl)]
	jj = -1

	for k in res:
		jj += 1
		n = len(k)
		matrix = [[0] * n for i in range(n)]
		for i in range(n):
			for j in range(n):
				if i != j:
					matrix[i][j] = _dist(k[i], k[j])

		# print("klast", k)
		res = _Komi(matrix)
		path = [k[res[0]-1]]
		for i in range(1, len(res)):
			if res[i] != res[i-1]:
				path.append(k[res[i]-1])

		# print(path)
		mi = 10**10
		mi_i = -1
		for i in range(len(path)):
			mi_di = _dist(st, path[i])
			if mi_di < mi:
				mi = mi_di
				mi_i = i

		ans_path = []
		i = mi_i
		while(i < len(path)):
			ans_path.append(path[i])
			i += 1

		i = 0
		while(i < mi_i):
			ans_path.append(path[i])
			i += 1

		ans_path.append(ans_path[0])

		for i in range(0, len(ans_path)):
			x = ans_path[i][0]
			y = ans_path[i][1]
			result[jj].append({
				# 'id': 0, # m[(x, y)],
				'numberInClaster': i,
				'numberOfClaster': jj,
				'description': "",
				'position': {'x': ans_path[i][0], 'y': ans_path[i][1]}
			})

	return(result)
