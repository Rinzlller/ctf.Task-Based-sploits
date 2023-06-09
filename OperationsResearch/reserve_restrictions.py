import matplotlib.pyplot as plt

cost = [67,12,45,10,234,123]
weight = [12,34,47,78,99,120]
n,rlblt = 6,[.4,.1,.5,.1,.9,.7]
cMax,wMax = 150,78

def about(x):
	r,c,w = 1,0,0
	for i in range(n):
		r *= 1-(1-rlblt[i])**(x[i]+1)
		c += cost[i]*x[i]
		w += weight[i]*x[i]
	return [r,c<=cMax and w<= wMax]

x = [0]*n
iMax = 0

while iMax != -1:
	iMax,deltaMax = -1,-1
	for i in range(n):
		xNew = x.copy()
		xNew[i] += 1
		delta = about(xNew)[0]-about(x)[0]
		delta /= cost[i]
		if delta > deltaMax and about(xNew)[1]:
			iMax,deltaMax = i,delta
	x[iMax] += 1
x[iMax] -= 1
# print( about(x),x )

fig, ax = plt.subplots()
ax.bar(range(len(x)), x)
ax.set_xlabel('Индекс элемента')
ax.set_ylabel('Размер резерва')
ax.set_title('План резервирования')
plt.show()