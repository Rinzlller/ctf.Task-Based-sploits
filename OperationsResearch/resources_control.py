#!/usr/bin/env python3

import matplotlib.pyplot as plt


def main():
	
	n = 7
	d = [30,10,25,12,5,20,50]
	C = [11,40,11,19,22,16,40]
	S = [10,7,6,12,3,8,9]
	L = [0,0,0,0,0,0,0]
	x = [100,100,100,100,100,100,100]
	y = [0,0,0,0,0,0,0]
	
	for i in range(1,n):
		y[i] = x[i-1]+y[i-1]-d[i-1]
	
	for i in range(n):
		L[i] = C[i]+S[i]*(x[i]-d[i])
		
		for j in range(d[i]):
			if L[i] > C[i]+S[i]*(j-d[i]):
				x[i] = j
			L[i] = (C[i]+S[i])*x[i]
		
	plt.scatter([i+1 for i in range(n)], x)
	plt.title("План заказов")
	plt.xlabel("День")
	plt.ylabel("Заказ")
	plt.show()


if __name__ == "__main__":
    main()