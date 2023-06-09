#!/usr/bin/env python3

import matplotlib.pyplot as plt

def main():

	cost=[25,68,66.6,110]
	pers=[2,1,2,1]
	perf=[7,40,58,70]
	money=390
	staff=7

	profit=[0]*4
	for i in range(4):
		profit[i]=perf[i]/(cost[i]*pers[i])
	_sorted = sorted(range(4), key=lambda i: profit[i])[::-1]
	
	equip = [0]*4
	for i in _sorted:
		n = min(money//cost[i],staff//pers[i])
		money-=cost[i]*n
		staff-=pers[i]*n
		equip[i]=n

	print( equip )
	print_diagram( equip )


def print_diagram(values):
	labels = [f'N{i+1}' for i in range(4)]
	fig, ax = plt.subplots()
	ax.pie(values, labels=labels, autopct='%1.0f%%')
	ax.set_title(f'Count of equipment{len(values)}')
	plt.show()


if __name__ == "__main__":
    main()