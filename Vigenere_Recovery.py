#!/usr/bin/env python3

def main():
	with open("CT.txt", "r") as f:
		ct = f.read()
	ct = ''.join(ct.split())

	# AVERAGE IC must be about 0.0686
	# (or choice the first MAX value)
	for key_len in range(1, 21):
		print( "{}\t|\t{:.4f}\t|".format(key_len, IC_average(ct, key_len)) )
	
	key_len = 17
	print()
	Chi_square_test(ct, key_len)


def IC_average(ct: str, key_len: int) -> int:

	ic = 0
	ic_average = 0
	for group_id in range(key_len):
		
		IDs = range(group_id, len(ct), key_len)
		group = [ct[id] for id in IDs]
		counts = [group.count(c) for c in set(group)]
		ic = sum([n*(n-1) for n in counts])/len(group)/(len(group)-1)
		ic_average += ic / key_len
	
	return ic_average


def Chi_square_test(ct: str, key_len: int):
	
	F = [0.082, 0.014, 0.028, 0.038, 0.131, 0.029, 0.020, 0.053, 0.064, 0.001, 0.004, 0.034, 0.025, 0.071, 0.080, 0.020, 0.001, 0.068, 0.061, 0.105, 0.025, 0.009, 0.015, 0.002, 0.020, 0.001]
	key = ""

	for key_id in range(key_len):

		IDs = range(key_id, len(ct), key_len)
		group = [ct[id] for id in IDs]
		chi_square_min = 1000000000
		key_char = ""

		for shift in range(26):
			group_shift = [chr((ord(g)-65-shift)%26+65) for g in group]

			f = [0] * 26
			chi_square = 0
			for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			# for c in set(group):
				f_i = group_shift.count(c)/len(group_shift)
				F_i = F[ord(c)-65]
				chi_square += pow(f_i - F_i, 2) / F_i

			# print( "{}\t{}\t{}".format(chr(shift+65), "".join(group_shift), chi_square) )
			if chi_square < chi_square_min:
				chi_square_min = chi_square
				key_char = chr(shift+65)

		key += key_char

	print(key)


if __name__ == "__main__":
	main()
