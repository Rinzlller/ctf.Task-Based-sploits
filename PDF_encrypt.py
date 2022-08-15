#!/usr/bin/env python3

import sys
import random
from math import gcd

	# b'\rp\x84\xd6U\xf9\xfe\x9d:' - fist 42 bytes in CT
	# b'%PDF-1.5\n' - fist 42 bytes in *.pdf (PT)

def main():

	# first_pt = b'%PDF-1.5\n'
	# first_ct = b'\rp\x84\xd6U\xf9\xfe\x9d:'

	# pt = b'%PDF'
	# ct = b'\rp\x84\xd6'

	# for a in range(1, 256):
	# 	if gcd(a, 256) == 1:
	# 		for b in range(1, 256):
	# 			if dec(ct, a, b) == pt: print( a, b )

	a = 169
	b = 160

	dt = open('../crypto_xmas_spirit/encrypted.bin', 'rb').read()

	res = dec(dt, a, b)

	f = open('../letter.pdf', 'wb')
	f.write(res)
	f.close()


def enc(dt, a=-1, b=-1):
	mod = 256
	if a == -1:
		while True:
			a = random.randint(1,mod)
			if gcd(a, mod) == 1: break
		b = random.randint(1,mod)

	res = b''
	for byte in dt:
		enc = (a*byte + b) % mod
		res += bytes([enc])
	return res, a, b


def dec(dt, a, b):
	mod = 256
	res = b''
	for byte in dt:
		x = byte - b
		while( x % a != 0 or x < 0 ):
			x += 256
		if x:
			x = x // a
			res += x.to_bytes((x.bit_length() + 7) // 8, "big") #ВАЖНО: С НУЛЁМ НЕ РОБИТ
		else:
			res += b'\x00'
	return res


if __name__ == '__main__':
	main()