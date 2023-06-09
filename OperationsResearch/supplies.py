#!/usr/bin/env python3

from math import * 

def print_model(modelname, q, t, n, c):
	delt = "#"*len(modelname)
	print(f"{delt}\n{modelname}\n{delt}")
	print(f"Оптимальный размер поставок: {q:.2f}")
	print(f"Интервал поставок: {t:.2f}")
	print(f"Оптимальное число поставок: {n:.2f}")
	print(f"Мин. годовые издержки: {c:.2f}")

R,Cz,suppInten=30,100,7
Cs,Cd,spenInten=6,3,3

modelname="МОДЕЛЬ С ПОСТОЯННЫМ РАЗМЕРОМ"
q_=sqrt(2*Cz*R/Cs)
z=sqrt(Cz*R/2/Cs)
t_=360*sqrt(2*Cz/R/Cs)
n_=sqrt(Cs*R/Cz/2)
costMin_=sqrt(2*Cz*R*Cs)
print_model(modelname, q_, t_, n_, costMin_)
print(f"Средний текущий запас: {z:.2f}\n")

modelname="МОДЕЛЬ С ПОСТОЯННЫМ ИНТЕНСИВНОСТЬЮ ПОСТУПЛЕНИЯ"
K1=sqrt(suppInten/(suppInten-spenInten))
q,t,t1,n=K1*q_,K1*t_,q_/suppInten,n_/K1
costMin=costMin_/K1
print_model(modelname, q, t, n, costMin)
print(f"Время поступления заказанной партии: {t1:.2f}\n")

modelname="МОДЕЛЬ С ДОПУЩЕНИЕМ ДЕФИЦИТА"
K2=sqrt((Cs+Cd)/Cd)
q,z,zMax,t,n=K2*q_,q_/K2,q-z,K2*t_,n_/K2
costMin=costMin_/K2
print_model(modelname, q, t, n, costMin)
print(f"Оптимальный нач. запас: {z:.2f}")
print(f"Макс. уровень текущего запаса: {zMax:.2f}\n")

modelname="ОБОБЩЕННАЯ ОДНОПРОДУКТИВНАЯ МОДЕЛЬ"
q,z,t=K2*K1*q_,q_/K2/K1,K2*t_*K1
costMin=costMin_/K2/K1
print_model(modelname, q, t, n, costMin)
print(f"Оптимальный нач. запас: {z:.2f}\n")

modelname="МОДЕЛЬ С ПОТЕРЕЙ НЕУДОВЛЕТВОРЕННЫХ ЗАКАЗОВ"
K3=Cs/Cd
k=sqrt(K1**2+K3)
t,n=t_*k,n_/k
q=(K1**2)*(q_**2)/k
costMin=(costMin_/K1**2)/k
print_model(modelname, q, t, n, costMin)