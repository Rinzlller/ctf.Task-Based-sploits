#!/usr/bin/env python3

from pwn import *

def main():
	s = remote("35.193.60.121", 1337)
	
	n = s.recv()
	ans = s.recv()
	print(n, ans)
	
	s.send(f(int(n), 2014, 1856).encode())
	good = s.recv()
	print(good)
	
	while True:
		data = s.recv().decode()
		n = data.split("\n")[1]
		print(data)
		if "access" in data:
			exit()
		else:
			s.send(f(int(n), 2014, 1856).encode())
			good = s.recv()
			print(good)

	s.close()


def f(n, a, b):
	while n >= 0:
		if n % b == 0:
			return "Yes\n"
		n -= a
	return "No\n"


if __name__ == "__main__":
    main()

    
