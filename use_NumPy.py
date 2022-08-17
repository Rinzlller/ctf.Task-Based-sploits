#!/usr/bin/env python3

from Crypto.Util.number import *
from numpy.polynomial import polynomial as P
from numpy import roots, absolute, gcd

def main():
	print(gcd(1273, 871))

	x = [1, 7, -30896910]
	# y = [1, -8, 19, -313, -14, 14011]
	# n = 445387271828582072260402517623224672881762...
	# polyN = [0] * 11 + [(-1)*n]
	# z = P.polyadd(P.polymul(x, y), polyN)

	# keys = absolute(roots(z)[10])
	print(roots(x))

	# test1 -> 816  337 -432 -388
	# test2 -> 848 -388 -310  109


if __name__ == "__main__":
    main()