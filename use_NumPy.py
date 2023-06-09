#!/usr/bin/env python3

from Crypto.Util.number import *
from numpy.polynomial import polynomial as P
from numpy import roots, absolute, gcd

def main():
	x = [1, -4, 4]
	# y = [1, -8, 19, -313, -14, 14011]
	# n = 445387271828582072260402517623224672881762...
	# polyN = [0] * 11 + [(-1)*n]
	# z = P.polyadd(P.polymul(x, y), polyN)

	# keys = absolute(roots(z)[10])
	print(roots(x))


def root(x, n):
    # Start with some reasonable bounds around the nth root.
    upper_bound = 1
    while upper_bound ** n <= x:
        upper_bound *= 2
    lower_bound = upper_bound // 2
    # Keep searching for a better result as long as the bounds make sense.
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        mid_nth = mid ** n
        if lower_bound < mid and mid_nth < x:
            lower_bound = mid
        elif upper_bound > mid and mid_nth > x:
            upper_bound = mid
        else:
            # Found perfect nth root.
            return mid
    return mid + 1


if __name__ == "__main__":
    main()