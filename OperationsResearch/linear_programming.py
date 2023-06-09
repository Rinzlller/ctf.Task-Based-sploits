#!/usr/bin/env python3

import matplotlib.pyplot as plt
from scipy.optimize import linprog

def main():

	var_count = int(input("Введите количество элементов: "))
	
	# c = [-1, -2]
	c = [0] * var_count
	for i in range(var_count):
		c[i] = int(input(f"Введите прибыль C[{i+1}]: "))
	
	rest_count = int(input("Введите количество ограничений: "))

	# t = [20, 10, 2]
	t = [0] * rest_count
	for i in range(rest_count):
		t[i] = int(input(f"Введите ресурс t[{i+1}]: "))

	# k = [[ 2,  1], [-4,  5], [ 1, -2]]
	k = [[0]*var_count for _ in range(rest_count)]
	for i in range(rest_count):
		for j in range(var_count):
			k[i][j] = int(input(f"Введите ограничение k[{i+1};{j+1}]: "))

	bounds = [(0, float("inf")) for _ in range(var_count)]

	result = linprog(
		c=c,
		A_ub=k,
		b_ub=t,
		# A_eq=[[-1, 5]],	# левая сторона равенства
		# b_eq=[15],		# правая сторона равенства
		bounds=bounds,
		method="revised simplex"
	)

	print( result )
	print_diagram( result.x )


def print_diagram(values):
	labels = [f'x{i+1}' for i in range(len(values))]
	fig, ax = plt.subplots()
	ax.pie(values, labels=labels, autopct='%1.1f%%')
	ax.set_title(f'Values of x1..x{len(values)}')
	plt.show()


if __name__ == "__main__":
    main()