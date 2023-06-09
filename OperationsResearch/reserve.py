import matplotlib.pyplot as plt

n = 6
cost = [67,12,45,10,234,123]
weight = [12,34,47,78,99,120]
rlblt = [.4,.1,.5,.1,.9,.7]
rMin = 0.4

def getR(x):
	r = 1
	for i in range(n):
		r *= 1-(1-rlblt[i])**x[i]
	return r

x = [1]*n
while getR(x) < rMin:
	iMax,deltaMax = -1,-1
	for i in range(n):
		xNew = x.copy()
		xNew[i] += 1
		delta = getR(xNew)-getR(x)
		delta /= cost[i]
		if delta > deltaMax:
			iMax,deltaMax = i,delta
	x[iMax] += 1
# print( getR(x),x )

fig, ax = plt.subplots()
ax.bar(range(len(x)), x)
ax.set_xlabel('Индекс элемента')
ax.set_ylabel('Размер резерва')
ax.set_title('План резервирования')
plt.show()